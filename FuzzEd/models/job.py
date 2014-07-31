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
from xml_backend import AnalysisResult, MincutResult, SimulationResult


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

    MINCUT_JOB = 'mincut'
    TOP_EVENT_JOB = 'topevent'
    SIMULATION_JOB = 'simulation'
    EPS_RENDERING_JOB = 'eps'
    PDF_RENDERING_JOB = 'pdf'

    JOB_TYPES = (
        (MINCUT_JOB, 'Cutset computation'),
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
    exit_code = models.IntegerField(null=True)  # Exit code for this job, NULL if pending

    def input_data(self):
        ''' Used by the API to get the input data needed for the particular job type.'''
        if self.kind in (Job.MINCUT_JOB, Job.TOP_EVENT_JOB, Job.SIMULATION_JOB):
            return self.graph.to_xml(), 'application/xml'
        elif self.kind in (Job.EPS_RENDERING_JOB, Job.PDF_RENDERING_JOB):
            return self.graph.to_tikz(), 'application/text'
        assert (False)

    def done(self):
        return self.exit_code is not None

    @property
    def requires_download(self):
        """
            Indicates if the result should be delivered directly to the frontend
            as file, or if it must be preprocessed with self.result_rendering().
        """
        return self.kind in [Job.EPS_RENDERING_JOB, Job.PDF_RENDERING_JOB]

    @property
    def result_titles(self):
        ''' 
            The result class knows how the titles should look like.
        '''
        if self.kind == self.TOP_EVENT_JOB:
            return Result.titles(Result.ANALYSIS_RESULT, self.graph.kind)
        elif self.kind == self.SIMULATION_JOB:
            return Result.titles(Result.SIMULATION_RESULT, self.graph.kind)
        elif self.kind == self.MINCUT_JOB:
            return Result.titles(Result.MINCUT_RESULT, self.graph.kind)
    
    def axis_titles(self):
        ''' 
        Computes labeling and axis scales for the analysis results menu 
        '''
        
        axis_titles = {
            'X_MIN':-0.05,                           # Min. value on the X axis.
            'X_MAX':1.05,                            # Max. value on the X axis.
            'Y_MIN':0,                               # Min value on the Y axis.
            'Y_MAX':1.0,                             # Max value on the Y axis.
            'Y_TICK_INTERVAL':1.0,                   # Interval in which values are labeled on the Y axis.
            'Y_MINOR_TICK_INTERVAL': 1.0/10,         # Cross stripe is shown after each mino tick.              
            'POINT_RADIUS':1                         # Radius of the points drawn in higcharts.
            }
        
        return axis_titles   
    
    @classmethod
    def exists_with_result(cls, graph, kind):
        ''' 
            Return an existing job object for that graph and job kind, but only
            if it was computed on the same graph data and has existing results.

            Theoretically, there is only one cached job left, since the new creation
            leads to deletion of old versions. We anyway prepare for the case of
            having multiple cached old results, by just using the youngest one.
        '''
        try:
            return Job.objects.filter(graph=graph, kind=kind, graph_modified=graph.modified, exit_code=0).order_by('-created')[0]    
        except:
            return None

    def result_download(self):
        """
            Returns an HttpResponse as direct file download of the result data.
        """
        response = HttpResponse()
        response['Content-Disposition'] = 'attachment; filename=graph%u.%s' % (self.graph.pk, self.kind)
        response.content = Result.objects.exclude(kind=Result.GRAPH_ISSUES).get(job=self).binary_value
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

    def interpret_value(self, xml_result_value, db_result):
        """
            Interpret the incoming result value and convert it to feasible JSON for storage.

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
                else:
                    # This is the tip of the triangle.
                    # If this is a crisp probability, then there is only the point above added.
                    # In this case, add another fake point to draw a strisaght line.
                    # points.append([alpha_cut.value_.lowerBound, 0])
                    pass

            # Points is now a wild collection of coordinates, were double values for the same X 
            # coordinate may occur. We sort it (since the JS code likes that) and leave only the 
            # largest Y values per X value.

            # If we have only one point, it makes no sense to draw a graph
            #TODO: Instead, we could draw a nice exponential curve for the resulting rate parameter
            #      This demands some better support for feeding the frontend graph rendering (Axis range etc.)
            if alphacut_count > 1:
                db_result.points = json.dumps(sorted(points))

            # Compute some additional statistics for the front-end, based on the gathered probabilities
            if len(points) > 0:
                db_result.minimum = min(points, key=lambda point: point[0])[0]  # left triangle border position
                db_result.maximum = max(points, key=lambda point: point[0])[0]  # right triangle border position
                db_result.peak = max(points, key=lambda point: point[1])[0]  # triangle tip position

        if hasattr(xml_result_value, 'reliability') and xml_result_value.reliability is not None:
            reliability = float(xml_result_value.reliability)
            db_result.reliability = None if math.isnan(reliability) else reliability

        if hasattr(xml_result_value, 'mttf') and xml_result_value.mttf is not None:
            mttf = float(xml_result_value.mttf)
            db_result.mttf = None if math.isnan(mttf) else mttf

        if hasattr(xml_result_value, 'nSimulatedRounds') and xml_result_value.nSimulatedRounds is not None:
            rounds = int(xml_result_value.nSimulatedRounds)
            db_result.rounds = None if math.isnan(rounds) else rounds

        if hasattr(xml_result_value, 'nFailures') and xml_result_value.nFailures is not None:
            failures = int(xml_result_value.nFailures)
            db_result.failures = None if math.isnan(failures) else failures

        if hasattr(xml_result_value, 'timestamp') and xml_result_value.timestamp is not None:
            timestamp = int(xml_result_value.timestamp)
            db_result.timestamp = None if math.isnan(timestamp) else timestamp
        else:
            # All analysis results not refering to a particular timestamp refer to the configured missionTime
            top_node = db_result.graph.top_node()
            if top_node:
                timestamp = top_node.get_property('missionTime')
                db_result.timestamp = None if math.isnan(timestamp) else timestamp


    def parse_result(self, data):
        """
            Parses the result data and saves the content to the database, 
            in relation to this job.
        """
        if self.requires_download:
            if self.kind == self.PDF_RENDERING_JOB:
                old_results = self.results.filter(graph=self.graph, kind=Result.PDF_RESULT)
                old_results.delete()
                db_result = Result(graph=self.graph, job=self, kind=Result.PDF_RESULT)
            elif self.kind == self.EPS_RENDERING_JOB:
                old_results = self.results.filter(graph=self.graph, kind=Result.EPS_RESULT)
                old_results.delete()
                db_result = Result(graph=self.graph, job=self, kind=Result.EPS_RESULT)
            db_result.binary_value = data
            db_result.save()
            return

        # Ok, it is not binary, it is true XML result data

        logger.debug("Parsing backend result XML into database: \n"+str(data))
        doc = xml_backend.CreateFromDocument(str(data))

        # Delete old graph issues from a former analysis run
        self.graph.delete_results(kind=Result.GRAPH_ISSUES)

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
            # Node configurations can be bulk-inserted, since nobody links to them
            # The expensive looped Configuration object creation cannot be bulk-inserted,
            # since we need their pk's in the NodeCOnfiguration object
            db_nodeconfs = []
            for configuration in doc.configuration:
                db_conf = Configuration(graph=self.graph, costs=configuration.costs if hasattr(configuration, 'costs') else None)
                db_conf.save()
                conf_id_mappings[configuration.id] = db_conf
                logger.debug("Storing DB configuration %u for XML configuration %s in graph %u"%(db_conf.pk, configuration.id, self.graph.pk))
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
                    db_nodeconfs.append(db_nodeconf)
            logger.debug("Performing bulk insert of node configurations")
            NodeConfiguration.objects.bulk_create(db_nodeconfs)

        if hasattr(doc, 'result'):
            # Remove earlier results of the same kind
            if self.kind == self.TOP_EVENT_JOB:
                self.graph.delete_results(kind=Result.ANALYSIS_RESULT)
            elif self.kind == self.SIMULATION_JOB:
                self.graph.delete_results(kind=Result.SIMULATION_RESULT)
            elif self.kind == self.MINCUT_JOB:
                self.graph.delete_results(kind=Result.MINCUT_RESULT)
            db_results = []
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
                self.interpret_value(result, db_result)
                if result.issue:
                    db_result.issues = json.dumps(self.interpret_issues(result.issue))
                db_results.append(db_result)                    
            logger.debug("Performing bulk insert of parsed results")
            Result.objects.bulk_create(db_results)

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

