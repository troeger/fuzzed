from fabric.api import task, env, roles
from fabfile.common import version
from fabric.operations import put, run, sudo
import os.path
import os, ConfigParser

# Determine deployment target hosts from central settings file
conf = ConfigParser.ConfigParser()
conf.read('settings.ini')
webserver = conf.get('production','deployment_web_host')
backend = conf.get('production','backend_daemon_host')

env.roledefs['web'] = ['root@'+webserver]
env.roledefs['backend'] = ['root@'+backend]

@task
@roles('web')
def web():
    '''Performs deployment of the local packaging result on the web servers.'''
    package = "FuzzEd-"+version+".tar.gz"
    assert(os.path.isfile('dist/'+package))
    # TODO: Use bootstrap scripts for them, when they work in fabric mode
    # # Prepare environment on target machine
    # print "Preparing basic environment"
    # #sudo("apt-get update")
    # sudo('apt-get install apache2')	# already here for having /var/www
    # sudo('apt-get install gcc autoconf python python-dev python-pip')
    # sudo('pip install fabric')
    # TODO: Perform bootstrap.web stuff
    # TODO: Configure web server
    # Put release package
    print "Performing database backup"
    run('su -c "pg_dump -c -f /tmp/dbackup.sql fuzztrees" postgres')    
    print "Uploading "+package
    put('dist/'+package, '/var/www/fuzztrees.net/')
    run('tar xvfz /var/www/fuzztrees.net/'+package+" -C /var/www/fuzztrees.net/")
    print "Setting directory softlink"
    run('rm -f /var/www/fuzztrees.net/www')
    run('ln -fs /var/www/fuzztrees.net/FuzzEd-'+version+' /var/www/fuzztrees.net/www')
    #print "Storing backup of database, in case something goes wrong"
    #sudo('su - postgres; pg_dump fuzztrees > /tmp/fuzztrees_backup.sql')
    run('cd /var/www/fuzztrees.net/www/; ./manage.py syncdb --migrate')
    sudo('apache2ctl configtest')
    print "Restarting web server"
    sudo('service apache2 restart')

@task
@roles('backend')
def backend():
    ''' Performs deployment of the local packaging result on the backend server.'''
    package = "FuzzEdBackend-"+version+".tar.gz"
    assert(os.path.isfile('dist/'+package))
    print "Uploading "+package
    sudo('mkdir -p /usr/local/fuzzed')
    put('dist/'+package, '/usr/local/fuzzed/')
    run('tar xvfz /usr/local/fuzzed/'+package+' -C /usr/local/fuzzed/')
    run('rm /usr/local/fuzzed/FuzzEdBackend')
    run('ln -fs /usr/local/fuzzed/FuzzEdBackend-'+version+' /usr/local/fuzzed/FuzzEdBackend')
    sudo('rm /etc/init.d/fuzzed-backend')
    sudo('ln -fs /usr/local/fuzzed/FuzzEdBackend/initscript.sh /etc/init.d/fuzzed-backend')
    sudo('chmod u+x /etc/init.d/fuzzed-backend')
    sudo('service fuzzed-backend start')

