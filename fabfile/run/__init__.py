from fabric.api import task
from subprocess import Popen
import sys

@task
def rendering():
    '''Runs the rendering backend service.'''
    rendering = Popen(["python","backends/rendering/renderServer.py"])
    if rendering.returncode != None:
        print "Error %u while starting rendering server"%rendering.returncode
        exit(-1)
    while 1:
        print "Press 'q' for quitting ..."
        line = sys.stdin.readline()
        if line.startswith('q'):
            rendering.terminate()
            exit(0)


@task
def tests():
    '''Runs all the tests.'''
    os.system('./manage.py test FuzzEd')
