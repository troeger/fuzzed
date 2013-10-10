''' 
This is the connector daemon for all backend services. It talks to the FuzzEd web application and retrieves new jobs.
Based on the retrieved job type, the according backend executable is called.

This script takes the path of the config file 'daemon.ini' as command-line argument. If not given, the config file
is searched in the current directory. It contains the database connection information and the details of the backends,
and is generated through 'fab build.configs' from the central settings file.

If you want this thing on a development machine for backend services, use 'fab run.backend'.
'''

import ConfigParser, sys, psycopg2, select, logging, urllib2

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('FuzzEd')

def server():
    # Read configuration
    assert(len(sys.argv) < 3)
    conf=ConfigParser.ConfigParser()
    if len(sys.argv) == 1:
        conf.readfp(open('./daemon.ini'))
    elif len(sys.argv) == 2:
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
    logger.info("Connected to PostgreSQL (%s)"%conn.server_version)

    # Set listen mode for the job kinds we know from our configuration
    for channel in backends.keys():
        cursor.execute("LISTEN %s;"%channel)

    # Start receiving loop for jobs
    while 1:
        logger.debug("Waiting for work ...")
        select.select([conn],[],[])
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop()
            if notify.channel in backends.keys():
                try:
                    logger.debug(str(notify)) 
                    # The server sends us the job URL as payload, so we can GET the input file and PUT the output files
                    if notify.channel == 'ping':
                        # The only intention of this job type is heartbeats, so there only an empty result PUT
                        urllib2.urlopen(notify.payload, data='')
                        pass
                    else:
                        # TODO run executable from configuration dictionary
                        pass
                except Exception as e:
                    logger.debug('Error: '+str(e))
                    pass

if __name__ == '__main__':
    server()