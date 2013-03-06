# This module provides pythonic access to the calculation analysis server
# that is currently implemented in Java
from FuzzEd import settings
import json, urllib

baseUrl = settings.CALC_TOPEVENT_SERVER

class InternalError(Exception):
	'''
	Denotes an internal error, such as XML serialization bugs, that cannot be fixed by the end user
	'''
	pass

def createJob(xml, decompositionNumber, verifyOnly=False):
	verifyflag = str(verifyOnly).lower()
	post_data = xml.encode('utf-8')
	conn=urllib.urlopen('%s/fuzztree/analysis/createJob?decompositionNumber=%u&verifyOnly=%s'%(baseUrl, decompositionNumber, verifyflag), post_data)	
	if conn.getcode() == 200:
		# Success, parse result to fetch job identifier
		result = json.loads(conn.read())
		logging.debug("Created job on calculation server: job id %u, %u configurations, %u nodes"%(result['jobid'], result['num_configurations'], result['num_nodes']))
		return result
	elif conn.getcode() == 400:
		e=InternalError("XML or decomposition number are ill-formatted")
		raise e
	else:
		e=InternalError("Unspecified internal error in calculation server")
		raise e


