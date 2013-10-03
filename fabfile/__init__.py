from fabric.api import task
from contextlib import contextmanager
import sys, os

sys.path.append('..')                       # Some of the sub-tasks import stuff from FuzzEd
import bootstrap, build, clean, package     # Import sub-tasks

@contextmanager
def created_dir(dirname):
    ''' Allows to operate in a subdirectory that is created, in case.'''
    try:
        os.mkdir(dirname)
    except:
        pass
    current = os.getcwd()
    os.chdir(dirname)
    yield
    os.chdir(current)



@task
def fixture_save(fname=None):
    '''Creates a test fixture from the current database in ./FuzzEd/fixtures/'''
    if fname==None:
        print "Usage: fab fixture_save:<filename>"
        return
    testaccount = {"model": "auth.user", "pk": 2,
        "fields": {
            "username" : "testadmin",
            "password" : "pbkdf2_sha256$10000$JNt1EZn2g72p$vX3UFh7g4mPa313pWW4lf4YxkUhL534V8/kxFaQ1XvM="
        }
    }
    jsontext = subprocess.check_output(['./manage.py','dumpdata','FuzzEd.node','FuzzEd.edge','FuzzEd.graph','FuzzEd.property'])
    data = json.loads(jsontext)
    data.append(testaccount)
    output=open("./FuzzEd/fixtures/"+fname,"w")
    output.write(json.dumps(data, indent=4))
    output.close()

@task
def fixture_load(fname=None):
    '''Loads the database with a test fixture from ./FuzzEd/fixtures/'''
    if fname==None:
        print "Usage: fab fixture_load:<filename>"
        return
    os.system('./manage.py loaddata ./FuzzEd/fixtures/'+fname)

@task
def run_tests():
    '''Runs all the tests.'''
    os.system('./manage.py test FuzzEd')




#TODO: Introduce DEPLOY task:
#    - Push the packaged release on the server(s).
#    - Trigger cuisine on production machine to update the software installation.
#    - Restart the web server / analysis server / rendering server.
#    - Extra fab tasks for web server / rendering server / analysis server deployment.
#    - Check for correct installation of init scripts.
#TODO: test how well this works with Vagrant for Linux dev machines


