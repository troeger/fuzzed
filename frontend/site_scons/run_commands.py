from SCons.Script import *

from subprocess import Popen
import sys
import os
import subprocess
import json


def run_backend(target, source, env):
    '''Runs the backend connector daemon, who serves all configured backends.'''
    os.chdir('backends')
    backend = Popen(["python", "daemon.py", "daemon.ini"])
    os.chdir('..')
    if backend.returncode is not None:
        print "Error %u while starting backend daemon" % backend.returncode
        exit(-1)
    print "Enter 'q' for quitting ..."
    while 1:
        line = sys.stdin.readline()
        if line.startswith('q'):
            backend.terminate()
            exit(0)


def run_frontend(target, source, env):
    '''Runs the server.'''
    os.system('./manage.py runserver')


def run_all(target, source, env):
    '''Runs the frontend and the backend.'''
    os.chdir('backends')
    backend = Popen(["python", "daemon.py", "daemon.ini"])
    os.chdir('..')
    os.system('./manage.py runserver')
    backend.terminate()


def fixture_save(target, source, env):
    '''Creates a test fixture from the current database.'''
    testaccount = {"model": "auth.user", "pk": 2,
                   "fields": {
                       "username": "testadmin",
                       "password": "pbkdf2_sha256$10000$JNt1EZn2g72p$vX3UFh7g4mPa313pWW4lf4YxkUhL534V8/kxFaQ1XvM="
                   }
                   }
    jsontext = subprocess.check_output(['./manage.py', 'dumpdata',
                                        'FuzzEd.project',
                                        'FuzzEd.graph',
                                        'FuzzEd.node',
                                        'FuzzEd.nodegroup',
                                        'FuzzEd.edge',
                                        'FuzzEd.property'])
    data = json.loads(jsontext)
    # Remove existing user account data, replace with test suite user
    for entry in data:
        if entry['model'] == 'auth.user':
            print "Replacing database user with test suite user"
            del entry
        if 'owner' in entry['fields']:
            entry['fields']['owner'] = 2   # see above
            print "Replacing database user reference for " + entry["model"]
    data.append(testaccount)
    output = open("FuzzEd/fixtures/new.json", "w")
    output.write(json.dumps(data, indent=4))
    print "New fixture file is now available at fixtures/new.json"
    output.close()

# def fixture_load(fname=None):
#    '''Loads the database with a test fixture from ./FuzzEd/fixtures/'''
#    if fname==None:
#        print "Usage: fab fixture_load:<filename>"
#        return
#    os.system('./manage.py loaddata ./FuzzEd/fixtures/'+fname)
