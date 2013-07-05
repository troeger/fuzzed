# This module provides pythonic access to the calculation analysis server
# that is currently implemented in Java
from FuzzEd import settings
from FuzzEd.models import xml_analysis, Node
import json, urllib, logging, time, xml.sax
import errors

logger   = logging.getLogger('FuzzEd')
BASE_URL = settings.ANALYZE_TOP_EVENT_PROBABILITY_SERVER

class InternalError(Exception):
    '''
    Denotes an internal error, such as XML serialization bugs, that cannot be fixed by the end user
    '''
    pass

class JobNotFoundError(Exception):
    '''
    Job not found in simulation backend
    '''
    pass

class AnalysisResultContentHandler(xml.sax.ContentHandler):

    def __init__(self):
        self.result = {}
        self.configurations = []
        self.warnings = {}
        self.errors = {}
        self.in_choice = False
        self.in_configuration = False
        self.in_alpha_cut = False
        self.choice_key = None
        self.choice_attributes = None
        self.in_probability = False
        self.alpha_cuts = None
        self.alpha_cut_key = None
        self.alpha_cut_values = None
        xml.sax.ContentHandler.__init__(self)

    def startElement(self, name, attrs):
        if 'AnalysisResult' in name:
            for key, value in attrs.items():
                if key in ['decompositionNumber', 'timestamp', 'validResult']:
                    self.result[key] = value

        elif name == 'configurations':
            self.in_configuration = True
            self.choices = {}
            self.config = {'costs': int(attrs.getValue('costs'))}

        elif name == 'choices' and self.in_configuration:
            self.in_choice = True
            # The choice key is a node ID that must be translated
            self.choice_key = int(Node.objects.get(pk=int(attrs.getValue('key'))).client_id)

        elif name == 'value' and self.in_choice and not self.in_alpha_cut:
            self.choice_attributes = {}
            for key, value in attrs.items():
                if key == 'xsi:type':
                    # strip XML namespace prefix from type identifier string
                    self.choice_attributes['type'] = value[value.find(':') + 1:]
                elif key == 'featureId':
                    # translate to client node ID
                    self.choice_attributes[key] = int(Node.objects.get(pk=int(value)).client_id)
                elif key == 'included':
                    self.choice_attributes[key] = (value == 'true')
                elif key == 'n':
                    self.choice_attributes[key] = int(value)
                else:
                    # its the type-specific value setting
                    self.choice_attributes[key] = value

        elif name == 'probability' and self.in_configuration:
            self.in_probability = True
            self.alpha_cuts = {}

        elif name == 'alphaCuts' and self.in_probability:
            self.in_alpha_cut = True
            self.alpha_cut_key = attrs.getValue('key')

        elif name == 'value' and not self.in_choice and self.in_alpha_cut:
            self.alpha_cut_values = [float(attrs.getValue('lowerBound')), float(attrs.getValue('upperBound'))]

        elif name == 'errors':
            node_id = int(Node.objects.get(pk=int(attrs.getValue('elementId'))).client_id)
            self.errors[node_id] = errors.text[int(attrs.getValue('issueId'))]

        elif name == 'warnings':
            node_id = int(Node.objects.get(pk=int(attrs.getValue('elementId'))).client_id)
            self.warnings[node_id] = errors.text[int(attrs.getValue('issueId'))]

    def endElement(self, name):
        if name == 'choices':
            self.in_choice = False
            self.choices[self.choice_key] = self.choice_attributes
        elif name == 'configurations':
            self.in_configuration = False
            self.config['choices'] = self.choices
            self.configurations.append(self.config)
        elif name == 'probability':
            self.in_probability = False
            self.config['alphaCuts'] = self.alpha_cuts
        elif name == 'alphaCuts':
            self.in_alpha_cut = False
            self.alpha_cuts[self.alpha_cut_key] = self.alpha_cut_values
 
    def characters(self, content):
        pass

    def as_json(self):
        self.result['configurations'] = self.configurations
        self.result['errors'] = self.errors
        self.result['warnings'] = self.warnings
        return json.dumps(self.result)
  
def analysis_result_as_json(xml_text):
    parsed_content = AnalysisResultContentHandler()
    xml.sax.parseString(xml_text, parsed_content)
    return parsed_content.as_json()

def create_job(xml, decomposition_number, verify_only=False):
    verify = str(verify_only).lower()
    post_data = xml.encode('utf-8')
    try:
        connection = urllib.urlopen('%s/fuzztree/analysis/createJob?decompositionNumber=%d&verifyOnly=%s'
                                    % (BASE_URL, decomposition_number, verify), post_data)
    except:
        raise InternalError('Sorry, the analysis service is unavailable at the moment.')        

    if connection.getcode() == 200:
        # Success, parse result to fetch job identifier
        data = connection.read().replace('\'', '"')
        logger.debug('Server result: ' + data)

        result = json.loads(data)
        job_id = result['jobid']
        num_configurations = result['num_configurations']
        num_nodes = result['num_nodes']
        logger.debug('Created job on calculation server: job id %d, %d configurations, %d nodes'
                     % (job_id, num_configurations, num_nodes))

        return job_id, num_configurations, num_nodes

    elif connection.getcode() == 400:
        raise InternalError('XML or decomposition number are ill-formatted')

    raise InternalError('Unspecified internal error in calculation server')

def get_job_result(job_id):
    '''
    Returns job result as XML, or None if the job is still running.
    Throws JobNotFoundError exception when the jobID is invalid.
    '''
    connection = urllib.urlopen('%s/fuzztree/analysis/getJobResult?jobId=%s' % (BASE_URL, job_id))

    if connection.getcode() == 200:
        jobs = connection.read()
        logger.debug('Server result: %s' % jobs)
        return analysis_result_as_json(jobs)
    elif connection.getcode() == 202:
        return None
    elif connection.getcode() == 400:
        raise InternalError('Job Id is not an integer')
    elif connection.getcode() == 404:
        raise JobNotFoundError()

    raise InternalError('Unspecified internal error in calculation server')

def abort_job(job_id):
    '''
    Abort the job. Returns True when the job abort succeeded,
    or False when the job was already completed or failed.
    '''
    connection = urllib.urlopen('%s/fuzztree/analysis/abortJob?jobId==%s' % (BASE_URL, job_id))

    if connection.getcode() == 200:
        return True
    elif connection.getcode() == 405:
        return False
    elif connection.getcode() == 400:
        raise InternalError('Job Id is not an integer')
    elif connection.getcode() == 404:
        raise JobNotFoundError()

    raise InternalError('Unspecified internal error in calculation server')

def list_jobs():
    '''
    List all jobs running in the simulation server.
    Returns a dictionary of jobs, where the value is
    'c' for completed, 'f' for failed and 'r' for running
    '''
    connection = urllib.urlopen('%s/fuzztree/analysis/listJobs' % BASE_URL)

    if connection.getcode() != 200:
        raise InternalError('Unspecified internal error in calculation server')

    received_jobs = connection.read().strip()
    if received_jobs == '()':
        return {}

    return {job_id: status for job_id, status in json.loads(received_jobs)}
