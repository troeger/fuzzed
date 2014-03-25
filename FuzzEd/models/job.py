from django.db import models, connection, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from django.core.mail import mail_managers
from graph import Graph
from node import Node
from result import Result
from configuration import Configuration
from node_configuration import NodeConfiguration
from south.modelsinspector import add_introspection_rules
from FuzzEd.models import xml_analysis, xml_simulation
from FuzzEd import settings
from FuzzEd.middleware import HttpResponseServerErrorAnswer
import uuid, json, xmlrpclib, math

from xml_configurations import FeatureChoice, InclusionChoice, RedundancyChoice, TransferInChoice

import logging
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
    CUTSETS_JOB       = 'cutsets'
    TOP_EVENT_JOB     = 'topevent'
    SIMULATION_JOB    = 'simulation'
    EPS_RENDERING_JOB = 'eps'
    PDF_RENDERING_JOB = 'pdf'    

    JOB_TYPES = (
        (CUTSETS_JOB,       'Cutset computation'),
        (TOP_EVENT_JOB,     'Top event calculation (analytical)'),
        (SIMULATION_JOB,    'Top event calculation (simulation)'),
        (EPS_RENDERING_JOB, 'EPS rendering job'),
        (PDF_RENDERING_JOB, 'PDF rendering job')
    )

    graph          = models.ForeignKey(Graph, null=True, related_name='jobs')
    graph_modified = models.DateTimeField()                                  # Detect graph changes during job execution
    secret         = models.CharField(max_length=64, default=gen_uuid)       # Unique secret for this job
    kind           = models.CharField(max_length=127, choices=JOB_TYPES)
    created        = models.DateTimeField(auto_now_add=True, editable=False)
    exit_code      = models.IntegerField(null=True)                          # Exit code for this job, NULL if pending

    def input_data(self):
        ''' Used by the API to get the input data needed for the particular job type.'''
        if self.kind in (Job.CUTSETS_JOB, Job.TOP_EVENT_JOB, Job.SIMULATION_JOB):
            return self.graph.to_xml(), 'application/xml'
        elif self.kind in (Job.EPS_RENDERING_JOB, Job.PDF_RENDERING_JOB):
            return self.graph.to_tikz(), 'application/text'
        assert(False)

    def done(self):
        return self.exit_code is not None

    def get_absolute_url(self):
        ''' Determine URL for the job result, when available for download. '''
        assert(self.requires_download())
        return reverse('frontend_graph_download', args=[self.graph.pk]) + "?format="+self.kind

    def requires_download(self):
        ''' Indicates if the result should be delivered directly to the frontend
            as file, or if it must be preprocessed with self.result_rendering().'''
        return self.kind in [Job.EPS_RENDERING_JOB, Job.PDF_RENDERING_JOB]

    def result_rendering(self):
            ''' Returns the job result as something that the frontend understands.'''
            json_result = {}
            errors = {}
            warnings = {}
            isValid = True

            assert(self.result)
            result_data = str(self.result)
            logger.debug("Rendering result data for frontend:")
            topId = self.graph.top_node().client_id

            # Parse analysis result XML file
            if (self.kind == Job.TOP_EVENT_JOB):
                doc = xml_analysis.CreateFromDocument(result_data)
            elif (self.kind == Job.SIMULATION_JOB):
                doc = xml_simulation.CreateFromDocument(result_data)
            else:
                assert(False)

            # Check global (problem) issues that are independent from the particular configuration
            # and were sent as part of the analysis result
            # Since the frontend always wants error messages as part of a graph element, 
            # we attach them to the TOP event for the moment (check issue #181)
            # TODO: This will break for RBD analysis, since there is no top event
            if hasattr(doc, 'issue'):
                graphErrors = []
                graphWarnings = []
                for issue in doc.issue:
                    if issue.message and len(issue.message)>0:
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
            if len(results)==0:
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
                            errors[issue.elementId]=issue.message
                        else:
                            warnings[issue.elementId]=issue.message

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
                    logging.debug("Probability: "+str(result.probability))
                    alphacut_count = len(result.probability.alphaCuts)  # we don't believe the delivered decomp_number
                    for alpha_cut in result.probability.alphaCuts:
                        y_val = alpha_cut.key+1 / alphacut_count        # Alphacut indexes start at zero
                        assert(0 <= y_val <= 1)
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
                    current_config['min']  = min(points, key=lambda point: point[0])[0]          # left triangle border position
                    current_config['max']  = max(points, key=lambda point: point[0])[0]          # right triangle border position
                    current_config['peak'] = max(points, key=lambda point: point[1])[0]          # triangle tip position
                    current_config['ratio'] = float(current_config['peak'] * current_config['costs']) if current_config['costs'] else None
                elif (self.kind == Job.SIMULATION_JOB):
                    reliability = float(result.reliability)
                    current_config['reliability'] = None if math.isnan(reliability) else reliability
                    mttf = float(result.mttf)
                    current_config['mttf'] = None if math.isnan(mttf) else mttf
                    rounds = int(result.nSimulatedRounds)
                    current_config['rounds'] = None if math.isnan(rounds) else rounds
                    failures = int(result.nFailures)
                    current_config['failures'] = None if math.isnan(failures) else failures
                    current_config['ratio'] = float(1-reliability * current_config['costs']) if current_config['costs'] else None

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
                        element     = choice.value_
                        json_choice = {}

                        if isinstance(element, FeatureChoice):
                            json_choice['type']      = 'FeatureChoice'
                            json_choice['featureId'] = element.featureId
                        elif isinstance(element, InclusionChoice):
                            json_choice['type']     = 'InclusionChoice'
                            json_choice['included'] = element.included
                        elif isinstance(element, RedundancyChoice):
                            json_choice['type'] = 'RedundancyChoice'
                            json_choice['n']    = int(element.n)
                        else:
                            raise ValueError('Unknown choice %s' % element)
                        json_choices[choice.key] = json_choice
                current_config['choices'] = json_choices

                json_configs.append(current_config)
            json_result['configurations'] = json_configs
            
            json_result['columns'] = [  { 'mData': 'id',     'sTitle': 'Config' },
                                        { 'mData': 'min',    'sTitle': 'Min'    },
                                        { 'mData': 'peak',   'sTitle': 'Peak'   },
                                        { 'mData': 'max',    'sTitle': 'Max'    },
                                        { 'mData': 'costs',  'sTitle': 'Costs'  },
                                        { 'mData': 'ratio',  'sTitle': 'Risk'   }]
                                        
            json_result['errors']         = errors
            json_result['warnings']       = warnings
            json_result['validResult']    = str(isValid)
            json_result['decompositionNumber'] = str(decomp_number)

            return_data                   = json.dumps(json_result)
            logger.debug('Returning result JSON to frontend:\n' + return_data)

            return return_data

        #except Exception as e:
        #    mail_managers('Error on analysis result XML->JSON conversion', '%s\n\n%s' % (str(result_data), str(e),))
        #    raise HttpResponseServerErrorAnswer("We have an internal problem rendering your analysis result. Sorry! The developers are informed.")
    
    def parseResult(self, data):
        logger.debug('!!!begin_parseResult!!!\n\n')
                
        assert(data)
        assert(self.kind in [Job.TOP_EVENT_JOB, Job.SIMULATION_JOB])

        result_data = str(data)
        
        if  (self.kind == Job.TOP_EVENT_JOB):
            doc  = xml_analysis.CreateFromDocument(result_data)
            result_kind = Result.ANALYSIS_RESULT
             
        elif(self.kind == Job.SIMULATION_JOB):
            doc  = xml_simulation.CreateFromDocument(result_data)
            result_kind = Result.SIMULATION_RESULT
            
        # delete all previous results of this kind
        self.graph.results.filter(kind=result_kind).delete()
            
        ## Check global issues that are independent from the particular configuration
        ## Since the frontend always wants an elementID, we stitch them
        ## to the TOP event for the moment (check issue #181)
        ## TODO: This will break for RBD analysis, since there is no top event
        topId = self.graph.top_node().client_id
        graph_issues = {'errors':{}, 'warnings':{} }
        if hasattr(doc, 'issue'):
            graphErrors = []
            graphWarnings = []
            for issue in doc.issue:
                if issue.message and len(issue.message)>0:
                    if issue.isFatal:
                        graphErrors.append(issue.message)
                    else:
                        graphWarnings.append(issue.message)
            if len(graphErrors) > 0:
                graph_issues['errors'][topId] = graphErrors
            if len(graphWarnings) > 0:
                graph_issues['warnings'][topId] = graphWarnings
        
        logger.debug("Graph issues: "+str(graph_issues))
        graph_issues = Result(graph=self.graph, job=self, kind=Result.GRAPH_ISSUES, issues=json.dumps(graph_issues))
        graph_issues.save()        
                
        results = doc.result
        #TODO:  This will move to a higher XML hierarchy level in an upcoming schema update
        # For the moment, we assume that nobody needs that information later for rendering
        #decomposition = None
        #if hasattr(results[0], 'decompositionNumber'):
        #    decomposition = results[0].decompositionNumber
        
        # Go through all results
        for xmlresult in results:
             
            current_result = Result(graph=self.graph, kind=result_kind, job=self) 

            # Fetch issues hidden in maybe existing results
            node_issues = {'errors':{}, 'warnings':{} }
            if hasattr(xmlresult, 'issue'):
                for issue in xmlresult.issue:
                    if issue.isFatal:
                        node_issues['errors'][issue.elementId]=issue.message
                    else:
                        node_issues['warnings'][issue.elementId]=issue.message
                current_result.issues = json.dumps(node_issues)
                logger.debug("Issues: "+str(node_issues))
                        
            # Fetch probability used for graph rendering
            probability = []
            probability_sort = 0
            
            if (hasattr(xmlresult, 'probability') and self.kind == Job.TOP_EVENT_JOB and xmlresult.probability is not None):
                for alpha_cut in xmlresult.probability.alphaCuts:
                    probability.append([alpha_cut.value_.lowerBound, alpha_cut.key])
                    probability.append([alpha_cut.value_.upperBound, alpha_cut.key])
                    
                probability_sort = round(max(probability, key=lambda point: point[1])[0]*1000)  # Use peak value for probability_sort    
                current_result.value = json.dumps(probability)
                current_result.value_sort = probability_sort               
                logger.debug('probability: '      + str(probability))
                logger.debug('probability_sort: ' + str(probability_sort))
                 
            # Fetch rounds and failures if simulation job
            rounds   = None
            failures = None 
            if (self.kind == Job.SIMULATION_JOB):
                reliability = None if math.isnan(read_reliability) else float(xmlresult.reliability)
                rounds      = None if math.isnan(read_rounds) else int(xmlresult.nSimulatedRounds)
                failures    = None if math.isnan(read_failures) else int(xmlresult.nFailures)
                data = {'reliability': reliability, 'rounds': rounds, 'failures': failures}
                current_result.value = json.dumps(data)
                current_result.value_sort = reliability               
                logger.debug('Simulation result: '+str(data))
            
            # Fetch configuration if present (only FuzzTree has got configurations)
            if hasattr(xmlresult, 'configuration') and xmlresult.configuration is not None:                
                costs = xmlresult.configuration.costs if hasattr(xmlresult.configuration, 'costs') else None
                
                configuration = Configuration(graph = self.graph, costs=costs)
                configuration.save()
                current_result.configuration = configuration
                
                if hasattr(xmlresult.configuration, 'choice'):
                    for choice in xmlresult.configuration.choice:
                        client_id = choice.key
                        node    = Node.objects.get(client_id = client_id, graph=self.graph)
                        
                        element = choice.value_
                        setting = {}
                        if isinstance(element, FeatureChoice):
                            setting['type']      = 'FeatureChoice'
                            setting['featureId'] = element.featureId
                        elif isinstance(element, InclusionChoice):
                            setting['type']     = 'InclusionChoice'
                            setting['included'] = element.included
                        elif isinstance(element, RedundancyChoice):
                            setting['type'] = 'RedundancyChoice'
                            setting['n']    = int(element.n)
                        else:
                            raise ValueError('Unknown choice %s' % element)
                        
                        node_configuration = NodeConfiguration(configuration=configuration,
                                                               node=node, setting=setting)
                        node_configuration.save()
                      
                   
            current_result.save()
        
        logger.debug('!!!end_parseResult!!!\n\n\n')

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

        #TODO: job_files_url = 
        job_files_url    = settings.SERVER + reverse('job_files', kwargs={'job_secret': instance.secret})
        job_exitcode_url = settings.SERVER + reverse('job_exitcode', kwargs={'job_secret': instance.secret})

        try:
            # The proxy is instantiated here, since the connection should go away when finished
            s = xmlrpclib.ServerProxy(settings.BACKEND_DAEMON)
            logger.debug("Triggering %s job on url %s"%(instance.kind, job_files_url))
            s.start_job(instance.kind, job_files_url, job_exitcode_url)
        except Exception as e:
            mail_managers("Exception on backend call - "+settings.BACKEND_DAEMON,str(e))
            raise HttpResponseServerErrorAnswer("Sorry, we seem to have a problem with our FuzzEd backend. The admins are informed, thanks for the patience.")

