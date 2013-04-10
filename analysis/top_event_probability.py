# This module provides pythonic access to the calculation analysis server
# that is currently implemented in Java
from FuzzEd import settings
from FuzzEd.models import xml_analysis, Node
import json, urllib, logging

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

def analysis_result_as_json(xml_text):
    # load generating binding class with XML text
    try:
        xml = xml_analysis.CreateFromDocument(xml_text)
    except Exception as exception:
        logger.debug('Exception while parsing analysis XML: %s' % exception)
        raise InternalError

    # Create result dictionary to be converted to JSON
    result = {}
    result['decompositionNumber'] = xml.decompositionNumber
    result['timestamp'] = xml.timestamp

    # Result dictionary gets one entry for all error messages
    errors={}
    for error in xml.errors:
        client_id = Node.objects.get(pk=error.elementId).client_id
        errors[client_id] = error.message
        logger.debug('Analysis error for %s: %s' % (client_id, error.message))
    result['errors']=errors

    # Result dictionary gets one entry for all warning messages
    warnings={}
    for warning in xml.warnings:
        client_id = Node.objects.get(pk=warning.elementId).client_id
        warnings[client_id] = warning.message
        logger.debug('Analysis warning for %s: %s' % (client_id, warning.message))
    result['warnings']=warnings

    # Result dictionary gets one entry for all configurations and their results
    configurations = []
    for configuration in xml.configurations:
        # in each configuration, there is a particular choice for each of the variation points
        variation = {}
        choices   = {}

        for choice in configuration.choices:
            # determine the client id of the node that represents this variation point
            client_id = Node.objects.get(pk=choice.key).client_id
            if hasattr(choice.value_, 'n'):
                # This is a redundancy variation, with some choice for N
                choices[client_id] = {
                    'type':  'RedundancyChoice',
                    'value': choice.value_.n
                }

            elif hasattr(choice.value_, 'featureId'):
                # This is a feature variation, with a choice for the chosen client node in this config
                choices[client_id] = {
                    'type': 'FeatureChoice',
                    'value': Node.objects.get(pk=choice.value_.featureId).client_id
                }

            elif hasattr(choice.value_, 'included'):
                choices[client_id] = {
                    'type': 'InclusionChoice',
                    'value': choice.value_.included
                }
            else:
                raise InternalError('Internal error: Unsupported choice result in analysis XML')

        variation['choices'] = choices
        # in each configuration, there is one lower / upper bound result per alpha cut
        alpha_cuts = {}

        for alpha_cut in configuration.probability.alphaCuts:
            # according to the schema, each alphacutresult has max one value
            alpha_cuts[alpha_cut.key] = (alpha_cut.value_.lowerBound, alpha_cut.value_.upperBound)

        variation['alphacuts'] = alpha_cuts
        configurations.append(variation)

    result['configurations'] = configurations

    return json.dumps(result)

def create_job(xml, decomposition_number, verify_only=False):
    verify = str(verify_only).lower()
    post_data = xml.encode('utf-8')
    connection = urllib.urlopen('%s/fuzztree/analysis/createJob?decompositionNumber=%d&verifyOnly=%s'
                                % (BASE_URL, decomposition_number, verify), post_data)

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
