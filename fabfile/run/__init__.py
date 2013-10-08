from fabric.api import task
from subprocess import Popen
import sys, os

@task
def backend():
    '''Runs the backend connector daemon, who serves all configured backends.'''
    backend = Popen(["python","backends/daemon.py","backends/daemon.ini"])
    if backend.returncode != None:
        print "Error %u while starting backend daemon"%backend.returncode
        exit(-1)
    print "Enter 'q' for quitting ..."
    while 1:
        line = sys.stdin.readline()
        if line.startswith('q'):
            backend.terminate()
            exit(0)


@task
def tests():
    '''Runs all the tests.'''
    os.system('./manage.py test FuzzEd')
