''' 
This is the connector daemon for all backend services. It talks to the FuzzEd web application
and retrieves new jobs. Based on the retrieved job type, the according backend executable 
is called.

This script takes the path of the config file 'daemon.ini' as command-line argument. 
If not given, the config file is searched in the current directory. 
It is generated through 'fab build.configs' from the central settings file.

If you want this thing on a development machine for backend services, 
use 'fab run.backend', so that a potential Vagrant run is considered.
'''

import requests, ConfigParser, sys, select, logging, urllib2, tempfile, shutil, os, subprocess, threading
from SimpleXMLRPCServer import SimpleXMLRPCServer

# Initial configuration of logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('FuzzEd')

backends = {}
options = {}

useTestServer = False

class WorkerThread(threading.Thread):
    jobtype = ""
    joburl_status = ""
    joburl_files = ""

    def __init__(self, jobtype, joburl_files, joburl_exitcode):
        self.jobtype = jobtype
        self.joburl_exitcode = joburl_exitcode
        self.joburl_files = joburl_files
        threading.Thread.__init__(self)

    def sendFiles(self, url, files):
        logger.debug("Sending data to %s: %s"%(url, str(files)))
        r = requests.post(url, files=files, allow_redirects=False, verify=False)
        if r.text:
            logger.debug("Data sent, response was: "+str(r.text))

    def report_problem(self, exit_code):
        logger.debug("Sending exit code %s to %s"%(str(exit_code), self.joburl_exitcode))
        results = {'exit_code' : exit_code}
        r = requests.post(self.joburl_exitcode, data=results, verify=False)
        logger.debug("Error report sent, response was: "+str(r.text))

    def run(self):
        try:
            logger.info("Working for job URL: "+self.joburl_files)        

            # Create tmp directories
            tmpdir = tempfile.mkdtemp()
            tmpfile = tempfile.NamedTemporaryFile(dir=tmpdir, delete=False)

            # Fetch input data and store it
            input_data = urllib2.urlopen(self.joburl_files)
            tmpfile.write(input_data.read())
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
                if output_file.startswith("*"):
                    suffix = output_file[1:]
                    results = {fname: open(tmpdir+"/"+fname, "rb") for fname in os.listdir(tmpdir) if fname.endswith(suffix)}
                else:
                    results = {output_file: open(tmpdir+os.sep+output_file, "rb")}
                self.sendFiles(self.joburl_files, results)
            else:
                logger.error("Error on execution: Exit code "+str(exit_code))  
                logger.error("Saving input file for later reference: /tmp/lastinput.xml")
                os.system("cp %s /tmp/lastinput.xml"%tmpfile.name)
                self.report_problem(exit_code)

        except Exception as e:
            logger.debug('Exception, delivering -1 exit code to frontend: '+str(e))
            self.report_problem(-1)

        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

class JobServer(SimpleXMLRPCServer):

    def __init__(self, conf):
        SimpleXMLRPCServer.__init__(self, (options['backend_daemon_host'], int(options['backend_daemon_port'])))
        self.register_function(self.handle_request, 'start_job')

    def handle_request(self, jobtype, joburl_files, joburl_exitcode):
        logger.debug("Received %s job at %s"%(jobtype, joburl_files))
        if useTestServer:
            logger.debug("Patching job URL for test server support")
            parts = joburl_files.split('/',3)
            joburl_files = "http://localhost:8081/"+parts[3]      # LifeTestServer URL from Django docs
            parts = joburl_exitcode.split('/',3)
            joburl_exitcode = "http://localhost:8081/"+parts[3]      # LifeTestServer URL from Django docs
        if jobtype not in backends.keys():
            logger.error("Unknown job type "+jobtype)
            return False
        else:
            # Start worker thread for this task
            worker = WorkerThread(jobtype, joburl_files, joburl_exitcode)
            worker.start()
            return True

if __name__ == '__main__':
    # Read configuration
    assert(len(sys.argv) < 3)
    conf=ConfigParser.ConfigParser()
    if len(sys.argv) == 1:
        # Use default INI file in local directory
        conf.readfp(open('./daemon.ini'))
    elif len(sys.argv) == 2:
        if sys.argv[1] == "--testing":
            useTestServer = True
            conf.readfp(open('./daemon.ini'))
        else:
            useTestServer = False
            # Use provided INI file
            conf.readfp(open(sys.argv[1]))
    # Initialize logging, based on settings
    logger.addHandler(logging.FileHandler(conf.get('server','backend_log_file')))
    # Read backends from configuration
    for section in conf.sections():
        if section.startswith('backend_'):
            settings = dict(conf.items(section))
            backends[settings['job_kind']] = settings 
        elif section == 'server':
            options = dict(conf.items('server'))
    logger.info("Configured backends: "+str(backends.keys()))
    logger.info("Options: "+str(options))
    # Start server
    server = JobServer(conf)
    server.serve_forever()
