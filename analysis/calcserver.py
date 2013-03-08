# This module provides pythonic access to the calculation analysis server
# that is currently implemented in Java
from FuzzEd import settings
import json, urllib, logging

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
		resultXml = conn.read()
		logger.debug("Server result: "+str(resultXml))		
		return resultXml
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


