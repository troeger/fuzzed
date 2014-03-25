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

    def result(self):
        ''' Returns the result of this job so that it can directly go into a HTTTP Response.'''
        if self.kind in (Job.CUTSETS_JOB, Job.TOP_EVENT_JOB, Job.SIMULATION_JOB):
            # TODO: Get all configuration results + graph issues and stitch them together
            pass
        elif self.kind in (Job.EPS_RENDERING_JOB, Job.PDF_RENDERING_JOB):
            logger.debug("Delivering binary result as download.")
            return self.results.first().to_url()

    def parseResult(self, data):
        ''' 
            This method parses an incoming backend result and stores it in the database.
        '''

        logger.debug('!!!begin_parseResult!!!\n\n')

        # Determine result kind                
        if (self.kind == Job.PDF_RENDERING_JOB):
            doc = None
            result_kind = Result.PDF_RESULT

        elif (self.kind == Job.EPS_RENDERING_JOB):
            doc = None
            result_kind = Result.EPS_RESULT
     
        if  (self.kind == Job.TOP_EVENT_JOB):
            doc  = xml_analysis.CreateFromDocument(str(data))
            result_kind = Result.ANALYSIS_RESULT
             
        elif(self.kind == Job.SIMULATION_JOB):
            doc  = xml_simulation.CreateFromDocument(str(data))
            result_kind = Result.SIMULATION_RESULT
            
        # delete all previous results of this kind
        self.graph.results.filter(kind=result_kind).delete()

        if not doc:
            # Binary result, not XML result, just store it and leave
            result = Result(graph=self.graph, kind=result_kind, job=self, binary_value=data)
            result.save()
            return

        # We have a parsed XML result
            
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

