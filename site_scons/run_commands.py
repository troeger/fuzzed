from SCons.Script import * 

from subprocess import Popen
import sys, os, socket

def backend():
    '''Runs the backend connector daemon, who serves all configured backends.'''
    os.chdir('backends')
    backend = Popen(["python","daemon.py","daemon.ini"])
    os.chdir('..')
    if backend.returncode != None:
        print "Error %u while starting backend daemon"%backend.returncode
        exit(-1)
    print "Enter 'q' for quitting ..."
    while 1:
        line = sys.stdin.readline()
        if line.startswith('q'):
            backend.terminate()
            exit(0)

def server(target, source, env):
    '''Runs the server.'''
    ip = None
    # Perform new config build on every startup. 
    # This is basically intended for the case were somebody
    # permanently flips between native development and
    # Vagrant development. The backend daemon currently has
    # no Vagrant-specific settings, so we don't need to do the
    # same stunt in def backend()
    if socket.getfqdn() == 'vagrant-ubuntu-trusty-32':
        ip = "192.168.33.10"
        print 'Using Vagrant IP: ' + ip
        os.system('fab build.configs:target=vagrant')
        os.system('./manage.py runserver %s:8000' % ip)
    else:
        os.system('fab build.configs:target=development')
        os.system('./manage.py runserver')

def tests(test=None):
    '''Runs all the tests.'''
    os.system("fab build.configs")          # Makes sure that the configs match to the runtime environment for the test
    if test:
        os.system('./manage.py test FuzzEd.tests.'+test)
    else:
        os.system('./manage.py test FuzzEd.tests')

