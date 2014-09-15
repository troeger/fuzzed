from SCons.Script import * 
from contextlib import contextmanager
import os, tarfile

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


def package_backend(target, source, env):
    '''
    	Performs packaging of the backend server.
    	Relies on the succesfull build of configs (in production mode)
    	and the backends.
    '''
    with created_dir("dist"):
        inclusions = [
            ["../backends/lib", "lib"],
            ["../backends/initscript.sh", "initscript.sh"],
            ["../backends/daemon.py", "daemon.py"],
            ["../backends/daemon.ini", "daemon.ini"],
            ["../backends/rendering", "rendering"]
        ]
        exclusion_suffix= []
        exclusion_files = []
        exclusion_dirs = []

        def tarfilter(tarinfo):
            fname = tarinfo.name
            if tarinfo.isdir():
                for dirname in exclusion_dirs:
                    # if the filter is "/static", we still want to add "/static-release"
                    if fname.endswith(dirname) or dirname+os.sep in fname:
                        print "Skipping directory "+fname
                        return None
                print "Adding directory "+fname
                return tarinfo
            elif tarinfo.isfile():
                if fname in exclusion_files:
                    print "Skipping file "+fname
                    return None
                for suffix in exclusion_suffix:
                    if fname.endswith(suffix):
                        print "Skipping file "+fname
                        return None
                print "Adding file "+fname
                return tarinfo

        tar = tarfile.open(target[0]+".tar.gz","w:gz")
        for src, dest in inclusions:
            tar.add(src, arcname=target[0]+"/"+dest, filter=tarfilter)
        tar.close()

def package_web(target, source, env):
    '''Performs packaging of web server.'''
    print 'Performing relevant build steps.'
    os.system('fab build.css')
    os.system('fab build.xmlschemas')
    os.system('fab build.notations')
    os.system('fab build.shapes')
    os.system('fab build.configs:target=production')
    print 'Building compressed static files ...'
    # Use Django collectstatic, which triggers django-require optimization
    if os.system('./manage.py collectstatic -v3 --noinput') != 0:
        raise Exception('Execution of collectstatic failed. Please check the previous output.\n')
    with created_dir("dist"):
        inclusions = [
            ["../manage.py", "manage.py"],
            ["../FuzzEd", "FuzzEd"]
        ]
        exclusion_suffix=[".pyc", ".sqlite", ".orig"]
        exclusion_files = []
        exclusion_dirs =[
            "/FuzzEd/static",
            "/FuzzEd/fixtures"            
        ]

        def tarfilter(tarinfo):
            fname = tarinfo.name
            if tarinfo.isdir():
                for dirname in exclusion_dirs:
                    # if the filter is "/static", we still want to add "/static-release"
                    if fname.endswith(dirname) or dirname+os.sep in fname:
                        print "Skipping directory "+fname
                        return None
                print "Adding directory "+fname
                return tarinfo
            elif tarinfo.isfile():
                if fname in exclusion_files:
                    print "Skipping file "+fname
                    return None
                for suffix in exclusion_suffix:
                    if fname.endswith(suffix):
                        print "Skipping file "+fname
                        return None
                print "Adding file "+fname
                return tarinfo

        tar = tarfile.open(target[0]+".tar.gz","w:gz")
        for src, dest in inclusions:
            tar.add(src, arcname=target[0]+"/"+dest, filter=tarfilter)
        tar.close()

packageweb = Builder(action=package_web)
packagebackend = Builder(action=package_backend)
