from fabric.api import task, env, roles
from fabfile.common import version
from fabfile import bootstrap
from fabric.operations import put, run, sudo
import os.path

env.roledefs['web'] = ['root@93.180.157.101']
#env.roledefs['web'] = ['tb0.asg-platform.org']
env.roledefs['backends'] = ['t420.asg-platform.org']

@task
@roles('web')
def web():
    # '''Performs deployment on the web servers.'''
    # package = "FuzzEd-"+version+".tar.gz"
    # assert(os.path.isfile('dist/'+package))
    # # Prepare environment on target machine
    # print "Preparing basic environment"
    # #sudo("apt-get update")
    # sudo('apt-get install apache2')	# already here for having /var/www
    # sudo('apt-get install gcc autoconf python python-dev python-pip')
    # sudo('pip install fabric')
    # # Put release package
    # print "Uploading "+package
    # put('dist/'+package, '/var/www/')
    # run('tar xvfz /var/www/'+package+" -C /var/www/")
    # print "Setting directory softlink"
    # run('rm -f /var/www/FuzzEd')
    # run('ln -s /var/www/FuzzEd-'+version+' /var/www/FuzzEd')
    print "Installing additional software"
    #TODO: Get rid of local system assumption in bootstrap scripts
    #      switch to pure Fabric mode of operation
    bootstrap.web()

