# This module provides pythonic access to the calculation analysis server
# that is currently implemented in Java
from FuzzEd import settings
from FuzzEd.models import xml_analysis, Node

import json, urllib, logging, time, xml.sax

logger = logging.getLogger('FuzzEd')

baseUrl = settings.CALC_TOPEVENT_SERVER

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
        self.inChoice = False
        self.inConfiguration = False
        self.inAlphaCut = False
        xml.sax.ContentHandler.__init__(self)

    def startElement(self, name, attrs):
        if "AnalysisResult" in name:
            self.resultAttrs={}
            for k,v in attrs.items():
                if k in ['decompositionNumber','timestamp','validResult']:
                    self.result[k]=v
        elif name == "configurations":
            self.inConfiguration = True
            self.choices = {}
            self.config = {'costs': int(attrs.getValue('costs'))}
        elif name == "choices" and self.inConfiguration:
            self.inChoice = True
            # The choice key is a node ID that must be translated
            self.choiceKey = int(Node.objects.get(pk=int(attrs.getValue('key'))).client_id)
        elif name == 'value' and self.inChoice and not self.inAlphaCut:
            self.choiceAttributes={}
            for k,v in attrs.items():
                if k=='xsi:type':
                    # strip XML namespace prefix from type identifier string
                    self.choiceAttributes['type']=v[v.find(':')+1:]
                elif k=='featureId':
                    # translate to client node ID
                    self.choiceAttributes[k]=int(Node.objects.get(pk=int(v)).client_id)
                else:
                    # its the type-specific value setting
                    self.choiceAttributes[k] = v
        elif name == 'probability' and self.inConfiguration:
            self.inProbability = True
            self.alphaCuts = {}
        elif name == 'alphaCuts' and self.inProbability:
            self.inAlphaCut = True
            self.alphaCutKey = attrs.getValue('key')
        elif name == 'value' and not self.inChoice and self.inAlphaCut:
            self.alphaCutValues = [float(attrs.getValue('lowerBound')), float(attrs.getValue('upperBound'))]
        elif name == 'errors':
            nodeid = int(Node.objects.get(pk=int(attrs.getValue('elementId'))).client_id)
            self.errors[nodeid] = attrs.getValue('message')
        elif name == 'warnings':
            nodeid = int(Node.objects.get(pk=int(attrs.getValue('elementId'))).client_id)
            self.warnings[nodeid] = attrs.getValue('message')

    def endElement(self, name):
        if name == "choices":
            self.inChoice = False
            self.choices[self.choiceKey] = self.choiceAttributes
        elif name == "configurations":
            self.inConfiguration = False
            self.config['choices'] = self.choices
            self.configurations.append(self.config)
        elif name == 'probability':
            self.inProbability = False
            self.config['alphaCuts'] = self.alphaCuts
        elif name == 'alphaCuts':
            self.inAlphaCut = False
            self.alphaCuts[self.alphaCutKey] = self.alphaCutValues
 
    def characters(self, content):
        pass

    def as_json(self):
        self.result['configurations']=self.configurations
        self.result['errors']=self.errors
        self.result['warnings']=self.warnings
        return json.dumps(self.result)
  
def analysisResultAsJson(xmltext):
    start = time.clock()
    parsedContent = AnalysisResultContentHandler()
    result = xml.sax.parseString(xmltext, parsedContent)
    json = parsedContent.as_json()
    passed = time.clock()-start
    logger.info("Analysis XML parsing with SAX took %s"%passed)
    return json

def analysisResultAsJsonValidating(xmltext):
    # load generating binding class with XML text
    start = time.clock()
    try:
        xml = xml_analysis.CreateFromDocument(xmltext)
        passed = time.clock()-start
        logger.info("Analysis XML parsing took %s"%passed)
    except Exception as e:
        logger.debug("Exception while parsing analysis XML: "+str(e))
    # Create result dictionary to be converted to JSON
    result = {}
    result['decompositionNumber']=xml.decompositionNumber
    result['timestamp']=xml.timestamp
    # Result dictionary gets one entry for all error messages
    errors={}
    for error in xml.errors:
        client_id = Node.objects.get(pk=error.elementId).client_id
        errors[client_id]=error.message
        logger.debug("Analysis error for %s: %s"%(client_id, error.message))
    result['errors']=errors
    # Result dictionary gets one entry for all warning messages
    warnings={}
    for warning in xml.warnings:
        client_id = Node.objects.get(pk=warning.elementId).client_id
        warnings[client_id]=warning.message
        logger.debug("Analysis warning for %s: %s"%(client_id, warning.message))
    result['warnings']=warnings
    # Result dictionary gets one entry for all configurations and their results
    configs = []
    for conf in xml.configurations:
        config={}
        # in each configuration, there is a particular choice for each of the variation points
        choices = {}
        for choice in conf.choices:
            # determine the client id of the node that represents this variation point
            client_id = Node.objects.get(pk=choice.key).client_id
            if hasattr(choice.value_, 'n'):
                # This is a redundancy variation, with some choice for N
                choices[client_id] = {
                    'type': 'RedundancyChoice',
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
                logger.error("Internal error: Unsupported choice result in analysis XML")
                assert False
        config['choices']=choices
        # in each configuration, there is one lower / upper bound result per alpha cut
        acuts={}      
        for acut in conf.probability.alphaCuts:
            # according to the schema, each alphacutresult has max one value
            lowerBound = acut.value_.lowerBound
            upperBound = acut.value_.upperBound
            acuts[acut.key]=(lowerBound, upperBound)
        config['alphacuts']=acuts
        config['costs']=conf.costs
        configs.append(config)
    result['configurations']=configs
    jsontext = json.dumps(result)
    passed = time.clock()-start
    logger.info("Analysis XML to JSON generation took %s"%passed)
    return jsontext

def createJob(xml, decompositionNumber, verifyOnly=False):
    verifyflag = str(verifyOnly).lower()
    post_data = xml.encode('utf-8')
    conn=urllib.urlopen('%s/fuzztree/analysis/createJob?decompositionNumber=%u&verifyOnly=%s'%(baseUrl, decompositionNumber, verifyflag), post_data)    
    if conn.getcode() == 200:
        # Success, parse result to fetch job identifier
        data = conn.read()
        data = data.replace("'",'"')
        logger.debug("Server result: "+str(data))
        result = json.loads(data)
        jobid = result['jobid']
        num_configurations = result['num_configurations']
        num_nodes = result['num_nodes']
        logger.debug("Created job on calculation server: job id %u, %u configurations, %u nodes"%(jobid, num_configurations, num_nodes))
        return jobid, num_configurations, num_nodes
    elif conn.getcode() == 400:
        raise InternalError("XML or decomposition number are ill-formatted")
    else:
        raise InternalError("Unspecified internal error in calculation server")

def getJobResult(jobid):
    '''
    Returns job result as XML, or None if the job is still running.
    Throws JobNotFoundError exception when the jobID is invalid.
    '''
    conn=urllib.urlopen('%s/fuzztree/analysis/getJobResult?jobId=%u'%(baseUrl, int(jobid))) 
    if conn.getcode() == 200:
        start = time.clock()
        resultXml = conn.read()
        logger.debug("Server result: "+str(resultXml))      
        passed = time.clock()-start
        logger.info("Reading analysis server results took %s"%passed)
        return analysisResultAsJson(resultXml)
    elif conn.getcode() == 202:
        return None
    elif conn.getcode() == 400:
        raise InternalError("JobID is not an integer")
    elif conn.getcode() == 404:
        raise JobNotFoundError()
    else:
        raise InternalError("Unspecified internal error in calculation server")

def abortJob(jobid):
    '''
    Abort the job. Returns True when the job abort succeeded,
    or False when the job was already completed or failed.
    '''
    conn=urllib.urlopen('%s/fuzztree/analysis/abortJob?jobId==%u'%(baseUrl, jobid)) 
    if conn.getcode() == 200:
        return True
    elif conn.getcode() == 405:
        return False
    elif conn.getcode() == 400:
        raise InternalError("JobID is not an integer")
    elif conn.getcode() == 404:
        raise JobNotFoundError()
    else:
        raise InternalError("Unspecified internal error in calculation server")

def listJobs():
    '''
    List all jobs running in the simulation server.
    Returns a dictionary of jobs, where the value is
    'c' for completed, 'f' for failed and 'r' for running
    '''
    conn=urllib.urlopen('%s/fuzztree/analysis/listJobs'%(baseUrl))  
    if conn.getcode() == 200:
        result=conn.read().strip()
        if result == "()":
            return {}
        else:
            resulttuples = json.loads(result)
            return {jobid: status for jobid, status in resulttuples}
    else:
        raise InternalError("Unspecified internal error in calculation server")


