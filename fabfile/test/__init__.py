from fabric.api import task
import sys, os, socket

@task
def api(test=None):
    '''Runs all api tests.'''
    os.system("fab build.configs")          # Makes sure that the configs match to the runtime environment for the test
    if test:
        os.system('./manage.py test FuzzEd.tests.'+test)
    else:
        os.system('./manage.py test FuzzEd.tests')

@task
def js(test=None):
    '''Runs js unit tests.'''
    os.system('mocha-phantomjs FuzzEd/tests/js-tests/src/test_runner.html')
