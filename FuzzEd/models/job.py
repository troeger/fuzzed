import uuid
import json
import xmlrpclib
import math
import logging

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_managers
from django.http import HttpResponse
from south.modelsinspector import add_introspection_rules

from graph import Graph
from node import Node
from configuration import Configuration
from node_configuration import NodeConfiguration
from result import Result
from FuzzEd.models import xml_backend
from FuzzEd import settings
from FuzzEd.middleware import HttpResponseServerErrorAnswer
from xml_configurations import FeatureChoice, InclusionChoice, RedundancyChoice
from xml_backend import AnalysisResult


logger = logging.getLogger('FuzzEd')


class NativeXmlField(models.Field):
    def db_type(self, connection):
        return 'xml'


add_introspection_rules([], ['^FuzzEd\.models\.job\.NativeXmlField'])


def gen_uuid():
    return str(uuid.uuid4())


class Job(models.Model):
    class Meta:
        app_label = 'FuzzEd'

    # These strings must be lowercase, since they travel through PostgreSQL notification,
    # which makes everything lower case
    CUTSETS_JOB = 'cutsets'
    TOP_EVENT_JOB = 'topevent'
    SIMULATION_JOB = 'simulation'
    EPS_RENDERING_JOB = 'eps'
    PDF_RENDERING_JOB = 'pdf'

    JOB_TYPES = (
        (CUTSETS_JOB, 'Cutset computation'),
        (TOP_EVENT_JOB, 'Top event calculation (analytical)'),
        (SIMULATION_JOB, 'Top event calculation (simulation)'),
        (EPS_RENDERING_JOB, 'EPS rendering job'),
        (PDF_RENDERING_JOB, 'PDF rendering job')
    )

    graph = models.ForeignKey(Graph, null=True, related_name='jobs')
    graph_modified = models.DateTimeField()  # Detect graph changes during job execution
    secret = models.CharField(max_length=64, default=gen_uuid)  # Unique secret for this job
    kind = models.CharField(max_length=127, choices=JOB_TYPES)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    result = models.BinaryField(null=True)  # Result file for this job
    exit_code = models.IntegerField(null=True)  # Exit code for this job, NULL if pending

    def input_data(self):
        ''' Used by the API to get the input data needed for the particular job type.'''
        if self.kind in (Job.CUTSETS_JOB, Job.TOP_EVENT_JOB, Job.SIMULATION_JOB):
            return self.graph.to_xml(), 'application/xml'
        elif self.kind in (Job.EPS_RENDERING_JOB, Job.PDF_RENDERING_JOB):
            return self.graph.to_tikz(), 'application/text'
        assert (False)

    def done(self):
        return self.exit_code is not None

    def as_http_response(self):
        """
            Returns the job result as proper HTTP response, depending on the result type.
        """
        assert (self.exit_code == 0)
        if self.requires_download:
            return self.result_download()
        else:
            return self.result_json()

    @property
    def requires_download(self):
        """
            Indicates if the result should be delivered directly to the frontend
            as file, or if it must be preprocessed with self.result_rendering().
        """
        return self.kind in [Job.EPS_RENDERING_JOB, Job.PDF_RENDERING_JOB]

    def result_download(self):
        """
            Returns an HttpResponse as direct file download of the result data.
        """
        response = HttpResponse()
        response['Content-Disposition'] = 'attachment; filename=graph%u.%s' % (self.graph.pk, self.kind)
        response.content = self.result
        response['Content-Type'] = 'application/pdf' if self.kind == 'pdf' else 'application/postscript'
        return response

    def interpret_issues(self, xml_issues):
        """
            Interpret the incoming list of issues and convert to feasible JSON for storage.
        """
        errors = []
        warnings = []
        for issue in xml_issues:
            json_issue={'message':issue.message, 
                        'issueId':issue.issueId, 
                        'elementId': issue.elementId}
            if issue.isFatal:
                errors.append(json_issue)
            else:
                warnings.append(json_issue)
        return {'errors': errors, 'warnings': warnings}

    def interpret_value(self, xml_result_value):
        """
            Interpret the incoming result value and convert it to feasible JSON for storage.
            Secondly, the function return a plain integer representing the result
            for sorting purposes. 

            Fuzzy probability values as result are given for each alpha cut. Putting
            all the different values together forms a triangular membership function.
            Crisp probabilities are just a special case of this, were the membership
            function collapses to a straight vertical line.

            The method determines both a list of drawable diagram coordinates, 
            and the result values to be shown directly to the user.

            Diagram point determination:

            The X axis represents the unreliability value (== probability of failure), 
            the Y axis the membership function probability value for the given unreliability value.
            For each alpha cut, the backend returns us the points were the upper border of the 
            alphacut stripe is crossing the membership triangle.
            The lowest alphacut (0) has its upper border directly on the X axis.
            The highest alphacut has its upper border crossing the tip of the membership function. 
                
            The two points were the alphacut border touches the membership function are called 
            "[lower, upper]", the number of the alphacut is the "key".
            For this reason, "lower" and "upper" are used as X coordinates, 
            while the key is used as "Y" coordinate.

        """
        result = {}
        sort_value = 0
        if hasattr(xml_result_value, 'probability') and xml_result_value.probability is not None:
            points = []
            logging.debug("Probability: " + str(xml_result_value.probability))
            alphacut_count = len(xml_result_value.probability.alphaCuts)  # we don't believe the delivered decomp_number
            for alpha_cut in xml_result_value.probability.alphaCuts:
                y_val = alpha_cut.key + 1 / alphacut_count  # Alphacut indexes start at zero
                assert (0 <= y_val <= 1)
                points.append([alpha_cut.value_.lowerBound, y_val])
                if alpha_cut.value_.upperBound != alpha_cut.value_.lowerBound:
                    points.append([alpha_cut.value_.upperBound, y_val])
                    if alpha_cut.value_.upperBound > sort_value:
                        # Use the highest point in the membership function as sort value
                        sort_value = round(alpha_cut.value_.upperBound*100)                    
                else:
                    # This is the tip of the triangle.
                    # If this is a crisp probability, then there is only the point above added.
                    # In this case, add another fake point to draw a strisaght line.
                    # points.append([alpha_cut.value_.lowerBound, 0])
                    pass
            # Points is now a wild collection of coordinates, were double values for the same X 
            # coordinate may occur. We sort it (since the JS code likes that) and leave only the 
            # largest Y values per X value.
            result['points'] = sorted(points)

            # Compute some additional statistics for the front-end, based on the gathered probabilities
            if len(points) > 0:
                result['min'] = min(points, key=lambda point: point[0])[0]  # left triangle border position
                result['max'] = max(points, key=lambda point: point[0])[0]  # right triangle border position
                result['peak'] = max(points, key=lambda point: point[1])[0]  # triangle tip position
                #result['ratio'] = float(current_config['peak'] * current_config['costs']) if current_config['costs'] else None

        if hasattr(xml_result_value, 'reliability') and xml_result_value.reliability is not None:
            reliability = float(xml_result_value.reliability)
            sort_value = round(reliability)            
            result['reliability'] = None if math.isnan(reliability) else reliability

        if hasattr(xml_result_value, 'mttf') and xml_result_value.mttf is not None:
            mttf = float(xml_result_value.mttf)
            result['mttf'] = None if math.isnan(mttf) else mttf

        if hasattr(xml_result_value, 'rounds') and xml_result_value.nSimulatedRounds is not None:
            rounds = int(result.nSimulatedRounds)
            result['rounds'] = None if math.isnan(rounds) else rounds

        if hasattr(xml_result_value, 'nFailures') and xml_result_value.nFailures is not None:
            failures = int(result.nFailures)
            result['failures'] = None if math.isnan(failures) else failures
            #result['ratio'] = float(1 - reliability * current_config['costs']) if current_config['costs'] else None

        return result, sort_value

    def parse_result(self):
        """
            Parses the stored binary result data and saves the content to the database, 
            in relation to this job.
        """
        if self.requires_download:
            # no parsing needed, directly delivered to client
            return
        logger.debug("Parsing backend result XML into database")
        doc = xml_backend.CreateFromDocument(str(self.result))

        if hasattr(doc, 'issue'):
            # Result-independent issues (for the whole graph, and not per configuration),
            # are saved as special kind of result
            db_result = Result(graph=self.graph , job=self, kind=Result.GRAPH_ISSUES)
            db_result.issues = json.dumps(self.interpret_issues(doc.issue))
            db_result.save()

        conf_id_mappings = {}         # XML conf ID's to DB conf ID's

        if hasattr(doc, 'configuration'):
            # Throw away existing configurations information
            self.graph.delete_configurations()
            # walk through all the configurations determined by the backend, as shown in the XML
            for configuration in doc.configuration:
                db_conf = Configuration(graph=self.graph, costs=configuration.costs if hasattr(configuration, 'costs') else None)
                db_conf.save()
                conf_id_mappings[configuration.id] = db_conf
                logger.debug("Storing configuration %u for graph %u"%(db_conf.pk, self.graph.pk))
                # Analyze node configuration choices in this configuration
                assert(hasattr(configuration, 'choice'))    # according to XSD, this must be given
                for choice in configuration.choice:
                    element = choice.value_
                    json_choice = {}
                    if isinstance(element, FeatureChoice):
                        json_choice['type'] = 'FeatureChoice'
                        json_choice['featureId'] = element.featureId
                    elif isinstance(element, InclusionChoice):
                        json_choice['type'] = 'InclusionChoice'
                        json_choice['included'] = element.included
                    elif isinstance(element, RedundancyChoice):
                        json_choice['type'] = 'RedundancyChoice'
                        json_choice['n'] = int(element.n)
                    else:
                        raise ValueError('Unknown choice %s' % element)
                    db_node = Node.objects.get(client_id=choice.key, graph=self.graph)
                    db_nodeconf = NodeConfiguration(node=db_node, configuration = db_conf, setting=json_choice)
                    db_nodeconf.save()
                    logger.debug("Storing node configuration %u for node %u"%(db_nodeconf.pk, db_node.pk))

        if hasattr(doc, 'result'):
            for result in doc.result:
                assert(int(result.modelId) == self.graph.pk)
                db_result = Result(graph=self.graph , job=self)
                if result.configId in conf_id_mappings:
                    db_result.configuration=conf_id_mappings[result.configId]
                if type(result) is AnalysisResult:
                    db_result.kind = Result.ANALYSIS_RESULT
                elif type(result) is MincutResult:
                    db_result.kind = Result.MINCUT_RESULT
                elif type(result) is SimulationResult:
                    db_result.kind = Result.SIMULATION_RESULT
                db_result.value, db_result.value_sort = self.interpret_value(result)
                if result.issue:
                    db_result.issues = json.dumps(self.interpret_issues(result.issue))
                db_result.save()
                logger.debug(db_result)

    def result_json(self):
        """
            Returns an HttpResponse as JSON representation of the result data.
            This currently holds only for analysis result data.
        """
        return HttpResponse(status=200)


        json_result = {}
        errors = {}
        warnings = {}
        isValid = True

        assert (self.result)
        result_data = str(self.result)
        logger.debug("Rendering result data for frontend:")
        topId = self.graph.top_node().client_id

        # Parse analysis result XML file
        doc = xml_backend.CreateFromDocument(result_data)

        # Check global (problem) issues that are independent from the particular configuration
        # and were sent as part of the analysis result
        # Since the frontend always wants error messages as part of a graph element,
        # we attach them to the TOP event for the moment (check issue #181)
        # TODO: This will break for RBD analysis, since there is no top event
        if hasattr(doc, 'issue'):
            graphErrors = []
            graphWarnings = []
            for issue in doc.issue:
                if issue.message and len(issue.message) > 0:
                    if issue.isFatal:
                        graphErrors.append(issue.message)
                    else:
                        graphWarnings.append(issue.message)
            # TODO: Joining should be no longer needed when #181 is fixed, since we then get list value support
            if len(graphErrors) > 0:
                errors[topId] = ','.join(graphErrors)
            if len(graphWarnings) > 0:
                warnings[topId] = ','.join(graphWarnings)

        results = doc.result

        # There is no frontend support for the situation that some (not all) configurations are valid,
        # instead, it has only global validity support
        # We therefore compute our own valid flag
        if len(results) == 0:
            isValid = False
        else:
            for result in results:
                if hasattr(result, 'validResult') and not result.validResult:
                    isValid = False
                    break

        # Fetch issues hidden inside the analysis results
        for result in results:
            if hasattr(result, 'issue'):
                for issue in result.issue:
                    if issue.isFatal:
                        errors[issue.elementId] = issue.message
                    else:
                        warnings[issue.elementId] = issue.message

        #TODO:  This will move to a higher XML hierarchy level in an upcoming schema update
        if hasattr(results[0], 'decompositionNumber'):
            decomp_number = int(results[0].decompositionNumber)
        else:
            decomp_number = 1
        if hasattr(results[0], 'timestamp'):
            json_result['timestamp'] = results[0].timestamp

        # collect information about the identified configurations
        # TODO: If results are marked as invalid, show only the configurations
        json_configs = []
        for confignum, result in enumerate(results):

            # set configuration id, get the configuration costs from the xml
            current_config = {}
            current_config['id'] = '#%s' % confignum
            current_config['costs'] = result.configuration.costs if hasattr(result.configuration, 'costs') else None

            # Generate frontend rendering data for this particular configuration.
            # JSON points is the diagram data that the frontend just draws without interpretation.
            # The X axis represents the unreliability value (== probability of failure), the Y axis the membership
            # function probability value for the given unreliability value.
            # Membership functions are triangles, cut in horizontal stripes. The analysis delivers the result function
            # as points on a triangle. One alphacut is represented as the points were the upper border of the alphacut
            # stripe is crossing the membership triangle. The lowest alphacut (0) has its upper border directly on the
            # X axis. The last alphacut has its upper border crossing the tip of the triangle. The two points were
            # the alphacut border touches the triangle ara called "[lower, upper]", the number of the alphacut is the "key".
            # For this reason, "lower" and "upper" are used as X coordinates, while the key is used as "Y" coordinate.
            points = []
            if hasattr(result, 'probability') and self.kind == Job.TOP_EVENT_JOB and result.probability is not None:
                # This was an analysis job that resulted in fuzzy probability values, one per alpha-cut
                # Crisp probabilities are just a special case of this
                logging.debug("Probability: " + str(result.probability))
                alphacut_count = len(result.probability.alphaCuts)  # we don't believe the delivered decomp_number
                for alpha_cut in result.probability.alphaCuts:
                    y_val = alpha_cut.key + 1 / alphacut_count  # Alphacut indexes start at zero
                    assert (0 <= y_val <= 1)
                    points.append([alpha_cut.value_.lowerBound, y_val])
                    if alpha_cut.value_.upperBound != alpha_cut.value_.lowerBound:
                        points.append([alpha_cut.value_.upperBound, y_val])
                    else:
                        # For real triangles, there must be only one point when lower and upper are the same,
                        # since this is the tip of the triangle.
                        # If this is a crisp probability, then there is only the point above added.
                        # In this case, add another fake point to draw a strisaght line.
                        # points.append([alpha_cut.value_.lowerBound, 0])
                        pass
                # Points is now a wild collection of coordinates, were double values for the same X coordinate
                # may occur. We sort it (since the JS code likes that) and leave only the largest Y values
                # per X value
                current_config['points'] = sorted(points)

            # Compute some additional statistics for the front-end, based on the gathered probabilities
            if (self.kind == Job.TOP_EVENT_JOB and len(points) > 0):
                current_config['min'] = min(points, key=lambda point: point[0])[0]  # left triangle border position
                current_config['max'] = max(points, key=lambda point: point[0])[0]  # right triangle border position
                current_config['peak'] = max(points, key=lambda point: point[1])[0]  # triangle tip position
                current_config['ratio'] = float(current_config['peak'] * current_config['costs']) if current_config[
                    'costs'] else None
            elif (self.kind == Job.SIMULATION_JOB):
                reliability = float(result.reliability)
                current_config['reliability'] = None if math.isnan(reliability) else reliability
                mttf = float(result.mttf)
                current_config['mttf'] = None if math.isnan(mttf) else mttf
                rounds = int(result.nSimulatedRounds)
                current_config['rounds'] = None if math.isnan(rounds) else rounds
                failures = int(result.nFailures)
                current_config['failures'] = None if math.isnan(failures) else failures
                current_config['ratio'] = float(1 - reliability * current_config['costs']) if current_config[
                    'costs'] else None

                # fetch the alphacuts
            #                json_alphacuts = {}
            #                if hasattr(result, 'probability'):
            #                    for alpha_cut in result.probability.alphaCuts:
            #                        json_alphacuts[alpha_cut.key] = [
            #                            alpha_cut.value_.lowerBound,
            #                            alpha_cut.value_.upperBound
            #                        ]
            #                    current_config['alphaCuts'] = json_alphacuts

            # tell something about the choices
            json_choices = {}
            if hasattr(result.configuration, 'choice'):
                for choice in result.configuration.choice:
                    element = choice.value_
                    json_choice = {}

                    if isinstance(element, FeatureChoice):
                        json_choice['type'] = 'FeatureChoice'
                        json_choice['featureId'] = element.featureId
                    elif isinstance(element, InclusionChoice):
                        json_choice['type'] = 'InclusionChoice'
                        json_choice['included'] = element.included
                    elif isinstance(element, RedundancyChoice):
                        json_choice['type'] = 'RedundancyChoice'
                        json_choice['n'] = int(element.n)
                    else:
                        raise ValueError('Unknown choice %s' % element)
                    json_choices[choice.key] = json_choice
            current_config['choices'] = json_choices

            json_configs.append(current_config)
        json_result['configurations'] = json_configs

        json_result['errors'] = errors
        json_result['warnings'] = warnings
        json_result['validResult'] = str(isValid)
        json_result['decompositionNumber'] = str(decomp_number)

        return_data = json.dumps(json_result)
        logger.debug('Returning result JSON to frontend:\n' + return_data)

        return HttpResponse(return_data)

        #except Exception as e:
        #    mail_managers('Error on analysis result XML->JSON conversion', '%s\n\n%s' % (str(result_data), str(e),))
        #    raise HttpResponseServerErrorAnswer("We have an internal problem rendering your analysis result. Sorry! The developers are informed.")


@receiver(post_save, sender=Job)
def job_post_save(sender, instance, created, **kwargs):
    ''' Informs notification listeners.
        The payload contains the job URL prefix with a secret, 
        which allows the listener to perform according actions.
    '''
    if created:
        # The only way to determine our own hostname + port number at runtime in Django
        # is from an HttpRequest object, which we do not have here. 
        # Option 1 is to fetch this information from the HttpRequest and somehow move it here.
        # This works nice as long as LiveServerTestCase is not used, since the Django Test
        # Client still accesses the http://testserver URL and not the live server URL.
        # We therefore take the static approach with a setting here, which is overriden
        # by the test suite run accordingly

        # TODO: Use reverse() for this
        job_url = settings.SERVER + '/api/back/jobs/' + instance.secret

        try:
            # The proxy is instantiated here, since the connection should go away when finished
            s = xmlrpclib.ServerProxy(settings.BACKEND_DAEMON)
            logger.debug("Triggering %s job on url %s" % (instance.kind, job_url))
            s.start_job(instance.kind, job_url)
        except Exception as e:
            mail_managers("Exception on backend call - " + settings.BACKEND_DAEMON, str(e))
            raise HttpResponseServerErrorAnswer(
                "Sorry, we seem to have a problem with our FuzzEd backend. The admins are informed, thanks for the patience.")

