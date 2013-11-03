''' 
This is the connector daemon for all backend services. It talks to the FuzzEd web application and retrieves new jobs.
Based on the retrieved job type, the according backend executable is called.

This script takes the path of the config file 'daemon.ini' as command-line argument. If not given, the config file
is searched in the current directory. It contains the database connection information and the details of the backends,
and is generated through 'fab build.configs' from the central settings file.

If you want this thing on a development machine for backend services, use 'fab run.backend'.
'''

import ConfigParser, sys, psycopg2, select, logging, urllib2, tempfile, shutil, os, subprocess
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('FuzzEd')

# Register the streaming http handlers from poster package with urllib2
register_openers()

def server():
    # I will burn in hell for this.
    # There is no smart way to convince the Django code that it delivers the correct URL for a job
    # if we run the test suite. This is related to the usage of LiveServerTestCase in tests.py.
    # For this reason, we let the test suite start this code with "--testing" and patch the job host then.
    patch_host = False
    # Read configuration
    assert(len(sys.argv) < 3)
    conf=ConfigParser.ConfigParser()
    if len(sys.argv) == 1:
        # Use default INI file in local directory
        conf.readfp(open('./daemon.ini'))
    elif len(sys.argv) == 2:
        if sys.argv[1] == '--testing':
            # This is a test suite run, so we take the default INI and patch the database name
            # to connect to the test database for getting notifications
            logger.info("Using test database")
            conf.readfp(open('./daemon.ini'))
            conf.set('db','db_name', conf.get('db','db_test_name'))
            # And now we make sure that the received Job URL is patched
            patch_host = True
        else:
            # Use provided INI file
            conf.readfp(open(sys.argv[1]))

    # Parse list of available backends
    backends = {}
    for section in conf.sections():
        if section.startswith('backend_'):
            settings = dict(conf.items(section))
            backends[settings['job_kind']]=settings
    logger.info("Configured backends: "+str(backends.keys()))

    # Establish connection to central Postgres database for notifications
    options=dict(conf.items('db'))        
    conn = psycopg2.connect("host=%(db_host)s dbname=%(db_name)s user=%(db_user)s password=%(db_password)s"%options)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    logger.debug("Notification from:"+str(conn.dsn))

    # Set listen mode for the job kinds we know from our configuration
    for channel in backends.keys():
        cursor.execute("LISTEN %s;"%channel)

    # Start receiving loop for jobs
    while 1:
        logger.debug("Waiting for work ...")
        select.select([conn],[],[])
        conn.poll()
        logger.debug("Got data...")
        while conn.notifies:
            notify = conn.notifies.pop()
            logger.debug("Got notification on channel "+notify.channel)
            if notify.channel in backends.keys():
                try:
                    logger.debug(str(notify)) 
                    tmpdir = tempfile.mkdtemp()
                    tmpfile = tempfile.NamedTemporaryFile(dir=tmpdir, delete=False)
                    joburl = notify.payload
                    if patch_host:
                        joburl = joburl.replace("localhost:8000","localhost:8081")
                    logger.info("Working for job URL: "+joburl)
                    # Fetch input data and store it
                    input_data = urllib2.urlopen(joburl+'files')
                    tmpfile.write(input_data.read())
                    tmpfile.close()
                    # There trick is that we do not need to know the operational details of this job here,
                    # since the calling convention comes from daemon.ini and the input file format is determined
                    # by the web server on download.
                    # Alle backend executables are just expected to follow the same command-line pattern as render.py.
                    cmd = "%s %s %s %s"%(backends[notify.channel]['executable'], tmpfile.name, backends[notify.channel]['output'], tmpdir)
                    logger.info("Running "+cmd)
                    exit_code = os.system(cmd)
                    if exit_code == 0:
                        # Upload result file(s) with poster library, which fixes the multipart encoding for us
                        logger.info("Uploading result to "+joburl)
                        output_file = backends[notify.channel]['output']
                        if output_file.startswith("*"):
                            suffix = output_file[1:]
                            results = {fname: open(tmpdir+"/"+fname, "rb") for fname in os.listdir(tmpdir) if fname.endswith(suffix)}
                        else:
                            results = {output_file: open(tmpdir+os.sep+output_file, "rb")}
                        logger.debug("Sending results: "+str(results))
                        datagen, headers = multipart_encode(results)
                        request = urllib2.Request(joburl+'files', datagen, headers)
                    else:
                        logger.error("Error on execution: Exit code "+str(exit_code))  
                        logger.error("Saving input file for later reference: /tmp/lasterror.input")
                        os.system("cp %s /tmp/lasterror.input"%tmpfile.name)
                        results = {'exit_code':exit_code}
                        datagen, headers = multipart_encode(results)
                        request = urllib2.Request(joburl+'exitcode', datagen, headers)                        
                    urllib2.urlopen(request)                  
                except Exception as e:
                    logger.debug('Error: '+str(e))
                    pass
                finally:
                    shutil.rmtree(tmpdir, ignore_errors=True)

if __name__ == '__main__':
    server()