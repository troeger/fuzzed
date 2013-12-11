from django.db import models, connection, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from django.core.mail import mail_managers
from graph import Graph
from south.modelsinspector import add_introspection_rules
from FuzzEd.models import xml_analysis, xml_simulation
from FuzzEd import settings
from FuzzEd.middleware import HttpResponseServerErrorAnswer
import uuid, json, xmlrpclib

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
    result         = models.BinaryField(null=True)                           # Result file for this job
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
            topId = self.graph.top_node().client_id

            if (self.kind == Job.TOP_EVENT_JOB):
                doc = xml_analysis.CreateFromDocument(result_data)
            elif (self.kind == Job.SIMULATION_JOB):
                doc = xml_simulation.CreateFromDocument(result_data)
            else:
                assert(False)

            # Check global issues that are independent from the particular configuration
            # Since the frontend always wants an elementID, we stitch them
            # to the TOP event for the moment (check issue #181)
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

            # There is no frontend support for some (not all) valid configuration results in the analysis result
            # We therefore compute our own valid flag
            if len(results)==0:
                isValid = False
            else:
                for result in results:
                    if hasattr(result, 'validResult') and not result.validResult:
                        isValid = False
                        break

            # Fetch issues hidden in maybe existing results
            for result in results:
                if hasattr(result, 'issue'):
                    for issue in result.issue:
                        if issue.isFatal:
                            errors[issue.elementId]=issue.message
                        else:
                            warnings[issue.elementId]=issue.message

            #TODO:  This will move to a higher XML hierarchy level in an upcoming schema update
            if hasattr(results[0], 'decompositionNumber'):
                json_result['decompositionNumber'] = str(results[0].decompositionNumber)
            if hasattr(results[0], 'timestamp'):
                json_result['timestamp'] = results[0].timestamp

            # gather information about the configurations
            # TODO: If results are marked as invalid, show only the configurations
            json_configs = []
            for confignum, result in enumerate(results):
                # get the cost from the xml
                current_config = {}

                current_config['num'] = confignum

                if hasattr(result.configuration, 'costs'):
                    current_config['costs'] = result.configuration.costs
                else:
                    current_config['costs'] = "N/A"
                # TODO: Compute these values
                if (self.kind == Job.TOP_EVENT_JOB):
                    current_config['min'] = 0.0
                    current_config['peak'] = 0.0
                    current_config['max'] = 0.0
                    current_config['ratio'] = 0.0
                elif (self.kind == Job.SIMULATION_JOB):
                    current_config['reliability'] = 0.0
                    current_config['mttf'] = 0.0
                    current_config['ratio'] = 0.0

                # fetch the alphacuts
#                json_alphacuts = {}
#                if hasattr(result, 'probability'):
#                    for alpha_cut in result.probability.alphaCuts:
#                        json_alphacuts[alpha_cut.key] = [
#                            alpha_cut.value_.lowerBound,
#                            alpha_cut.value_.upperBound
#                        ]
#                    current_config['alphaCuts'] = json_alphacuts

                # prepare graph rendering data for this configuration
                json_points = []
                if hasattr(result, 'probability'):
                    for alpha_cut in result.probability.alphaCuts:
                        json_points.append([alpha_cut.value_.lowerBound, alpha_cut.key])
                        json_points.append([alpha_cut.value_.upperBound, alpha_cut.key])
                current_config['points'] = json_points

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

            json_result['errors']         = errors
            json_result['warnings']       = warnings
            json_result['validResult']    = str(isValid)
            return_data                   = json.dumps(json_result)
            logger.debug('Returning result JSON to frontend:\n' + return_data)

            return return_data

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

        #TODO: job_files_url = reverse('job_files', kwargs={'job_secret': instance.secret})
        job_files_url = '%s/api/jobs/%s' % (settings.SERVER, instance.secret,)

        try:
            # The proxy is instantiated here, since the connection should go away when finished
            s = xmlrpclib.ServerProxy(settings.BACKEND_DAEMON)
            logger.debug("Triggering %s job on url %s"%(instance.kind, job_files_url))
            s.start_job(instance.kind, job_files_url)
        except Exception as e:
            mail_managers("Exception on backend call - "+settings.BACKEND_DAEMON,str(e))
            raise HttpResponseServerErrorAnswer("Sorry, we seem to have a problem with the analysis backend. The admins are informed, thanks for the patience.")

