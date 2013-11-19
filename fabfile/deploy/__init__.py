from fabric.api import task, env, roles
from fabfile.common import version
from fabfile.common import version
import os.path

env.roledefs['web'] = ['tb0.asg-platform.org']
env.roledefs['backends'] = ['t420.asg-platform.org']

@task
@roles('web')
def web():
    '''Performs deployment on the web servers.'''
    package = "dist/FuzzEd-"+version+".tar.gz"
    assert(os.path.isfile(package))
    print "Deploying "+package
    # Prepare environment on target machine
    run('fab bootstrap.web')
