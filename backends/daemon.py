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

import ConfigParser, sys, select, logging, urllib2, tempfile, shutil, os, subprocess
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from SimpleXMLRPCServer import SimpleXMLRPCServer

# Register the streaming http handlers from poster package with urllib2
register_openers()

class JobServer(SimpleXMLRPCServer):
    backends = {}
    options = {}

    def __init__(self, conf):
        for section in conf.sections():
            if section.startswith('backend_'):
                settings = dict(conf.items(section))
                self.backends[settings['job_kind']] = settings 
            elif section == 'server':
                self.options = dict(conf.items('server'))
        logger.info("Configured backends: "+str(self.backends.keys()))
        logger.info("Options: "+str(self.options))
        SimpleXMLRPCServer.__init__(self, ('localhost', int(self.options['backend_daemon_port'])))
        self.register_function(self.handle_request, 'start_job')

    def report_problem(self, joburl, exit_code):
        results = {'exit_code':exit_code}
        datagen, headers = multipart_encode(results)
        request = urllib2.Request(joburl+'exitcode', datagen, headers)                        
        urllib2.urlopen(request)                  

    def handle_request(self, jobtype, joburl):
        logger.debug("Received %s job"%jobtype)
        if jobtype not in self.backends.keys():
            logger.error("Unknown job type "+jobtype)
            return False
        else:
            try:
                tmpdir = tempfile.mkdtemp()
                tmpfile = tempfile.NamedTemporaryFile(dir=tmpdir, delete=False)
                logger.info("Working for job URL: "+joburl)
                # Fetch input data and store it
                input_data = urllib2.urlopen(joburl+'files')
                tmpfile.write(input_data.read())
                tmpfile.close()
                # There trick is that we do not need to know the operational details 
                # of this job here, since the calling convention comes from daemon.ini 
                # and the input file format is determined by the web server on download.
                # Alle backend executables are just expected to follow the same 
                # command-line pattern as render.py.
                cmd = "%s %s %s %s %s"%(self.backends[jobtype]['executable'], 
                                        tmpfile.name, 
                                        tmpdir+os.sep+self.backends[jobtype]['output'],
                                        tmpdir,
                                        self.backends[jobtype]['log_file'])
                logger.info("Running "+cmd)
                exit_code = os.system(cmd)
                if exit_code == 0:
                    # Upload result file(s) with poster library, which fixes the multipart encoding for us
                    logger.info("Uploading result to "+joburl)
                    output_file = self.backends[jobtype]['output']
                    if output_file.startswith("*"):
                        suffix = output_file[1:]
                        results = {fname: open(tmpdir+"/"+fname, "rb") for fname in os.listdir(tmpdir) if fname.endswith(suffix)}
                    else:
                        results = {output_file: open(tmpdir+os.sep+output_file, "rb")}
                    logger.debug("Sending results: "+str(results))
                    datagen, headers = multipart_encode(results)
                    request = urllib2.Request(joburl+'files', datagen, headers)
                    urllib2.urlopen(request)                  
                else:
                    logger.error("Error on execution: Exit code "+str(exit_code))  
                    logger.error("Saving input file for later reference: /tmp/lastinput.xml")
                    os.system("cp %s /tmp/lastinput.xml"%tmpfile.name)
                    self.report_problem(joburl, exit_code)
            except Exception as e:
                logger.debug('Exception, delivering -1 exit code to frontend: '+str(e))
                self.report_problem(joburl, -1)
                return False
            finally:
                shutil.rmtree(tmpdir, ignore_errors=True)
            return True

if __name__ == '__main__':
    # Read configuration
    assert(len(sys.argv) < 3)
    conf=ConfigParser.ConfigParser()
    if len(sys.argv) == 1:
        # Use default INI file in local directory
        conf.readfp(open('./daemon.ini'))
    elif len(sys.argv) == 2:
        # Use provided INI file
        conf.readfp(open(sys.argv[1]))
    # Initialize logging, based on settings
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('FuzzEd')
    logger.addHandler(logging.FileHandler(conf.get('server','backend_log_file')))
    # Start server
    server = JobServer(conf)
    server.serve_forever()
