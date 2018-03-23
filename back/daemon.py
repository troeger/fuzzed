''' 
This daemon waits for XML-RPC request from an ORE web server to execute jobs.
Basically Celery done by ourselves.
'''

import configparser
import base64
import sys
import logging
import urllib.request, urllib.error, urllib.parse
import tempfile
import shutil
import os
import threading
import json
import argparse
import requests
from xmlrpc.server import SimpleXMLRPCServer

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('FuzzEd')

backends = {}

class WorkerThread(threading.Thread):
    jobtype = ""
    joburl = ""

    def __init__(self, jobtype, joburl):
        self.jobtype = jobtype
        self.joburl = joburl
        threading.Thread.__init__(self)

    def sendResult(self, exit_code, file_data=None, file_name=None):
        """
        :rtype : None
        """
        results = {'exit_code': exit_code}
        if file_data and file_name:
            results['file_name'] = file_name
            results['file_data'] = str(base64.b64encode(file_data))
        logger.debug("Sending result data to %s"%(self.joburl))
        headers = {'content-type': 'application/json'}
        r = requests.patch(self.joburl, data=json.dumps(results), verify=False, headers=headers)
        if r.text:
            logger.debug("Data sent, response was: "+str(r.text))

    def run(self):
        try:
            logger.info("Working for job URL: "+self.joburl)

            # Create tmp directories
            tmpdir = tempfile.mkdtemp()
            tmpfile = tempfile.NamedTemporaryFile(dir=tmpdir, delete=False)

            # Fetch input data and store it
            logger.debug("Fetching input data ...")
            input_data = urllib.request.urlopen(self.joburl).read()
            logger.debug("Fetched {0} bytes of input data.".format(len(input_data)))
            tmpfile.write(input_data)
#            logger.debug(input_data)
            tmpfile.close()

            # There trick is that we do not need to know the operational details 
            # of this job here, since the calling convention comes from daemon.ini 
            # and the input file format is determined by the web server on download.
            # Alle backend executables are just expected to follow the same 
            # command-line pattern as render.py.
            cmd = "%s %s %s %s %s"%(backends[self.jobtype]['executable'], 
                                    tmpfile.name, 
                                    tmpdir+os.sep+backends[self.jobtype]['output'],
                                    tmpdir,
                                    backends[self.jobtype]['log_file'])
            logger.info("Running "+cmd)
            output_file = backends[self.jobtype]['output']

            # Run command synchronousely and wait for the exit code
            exit_code = os.system(cmd)
            if exit_code == 0:
                logger.info("Exit code 0, preparing result upload")
                assert(not output_file.startswith("*"))     # multiple result file upload not implemented
                with open(tmpdir+os.sep+output_file, "rb") as fd:
                    data = fd.read()
                    self.sendResult(0, data, output_file)
#                    logger.debug(data)
            else:
                logger.error("Error on execution: Exit code "+str(exit_code))  
                logger.error("Saving input file for later reference: /tmp/lastinput.xml")
                os.system("cp %s /tmp/lastinput.xml"%tmpfile.name)
                self.sendResult(exit_code)

        except Exception as e:
            logger.debug('Exception, delivering -1 exit code to frontend: '+str(e))
            self.sendResult(-1)

        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)
            logger.debug('Terminating worker thread for job '+self.joburl)

class JobServer(SimpleXMLRPCServer):

    server_override = None

    def __init__(self, options):
        SimpleXMLRPCServer.__init__(self, (options['backend_daemon_host'], int(options['backend_daemon_port'])))
        if 'server' in options:
            self.server_override = options['server']
        self.register_function(self.handle_request, 'start_job')

    def handle_request(self, jobtype, joburl):
        logger.debug("Received %s job at %s"%(jobtype, joburl))
        if self.server_override:
            logger.debug("Changing job URL due to command-line override")
            parts = joburl.split('/',3)
            joburl = self.server_override + '/' + parts[3]      # LifeTestServer URL from Django docs
        if jobtype not in list(backends.keys()):
            logger.error("Unknown job type "+jobtype)
            return False
        else:
            # Start worker thread for this task
            worker = WorkerThread(jobtype, joburl)
            worker.start()
            return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description='ORE backend daemon.')
    parser.add_argument('-c', '--config', default='./daemon.ini', help='Daemon configuration file.')
    parser.add_argument('-s', '--server', default=None, help='Override for ORE web server machine and port. Example: "testserver:8000"')
    args = parser.parse_args()

    # Read configuration
    conf=configparser.ConfigParser(strict=False)
    conf.readfp(open(args.config))

    # Initialize logging, based on settings
    logger.addHandler(logging.FileHandler(conf.get('server','backend_log_file')))

    # Read backends from configuration
    for section in conf.sections():
        if section.startswith('backend_'):
            settings = dict(conf.items(section))
            backends[settings['job_kind']] = settings 
        elif section == 'server':
            options = dict(conf.items('server'))

    if args.server:
        options['server'] = args.server

    logger.info("Configured backends: "+str(list(backends.keys())))
    logger.info("Options: "+str(options))

    # Start server
    server = JobServer(options)
    server.serve_forever()
