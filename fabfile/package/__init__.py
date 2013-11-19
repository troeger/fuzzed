import os, ConfigParser, tarfile
from contextlib import contextmanager
from fabric.api import task

# determine version
conf = ConfigParser.ConfigParser()
conf.optionxform = str   # preserve case in keys    
conf.read('settings.ini')
version=dict(conf.items('all'))['VERSION']


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

#@task
def web_server():
    '''Performs packaging of web server.'''
    print 'Performing build, just in case.'
    os.system('fab build.all')
    print 'Building compressed static files ...'
    # Use Django collectstatic, which triggers django-require optimization
    if os.system('./manage.py collectstatic -v3 --noinput') != 0:
        raise Exception('Execution of collectstatic failed. Please check the previous output.\n')
    with created_dir("dist"):
        exclusion_suffix=[".pyc", ".sqlite", ".orig"]
        exclusion_files = []
        inclusions = [
            ["../manage.py", "manage.py"],
            ["../FuzzEd", "FuzzEd"],
        ]
        exclusion_dirs =[
            "../FuzzEd/static/",
            "../FuzzEd/fixtures/"            
        ]

        def add_filter(fname):
            if fname in exclusion_files:
                return False
            for suffix in exclusion_suffix:
                if fname.endswith(suffix):
                    return False

            for dirname in exclusion_dirs:
                if fname.startswith(dirname):
                    return False
            print "Adding "+fname

        basename="FuzzEd-%s"%version
        tar = tarfile.open(basename+".tar.gz","w:gz")
        for src, dest in inclusions:
            tar.add(src, arcname=basename+"/"+dest, exclude=add_filter)
        tar.close()

#@task
#def analysis_server():
#    '''Performs packaging of analysis server. Assumes successful build.'''
#    current = os.getcwd()
#    os.chdir('dist')#

#    basename="FuzzEdAnalysis-%s"%__version__
#    tar = tarfile.open(basename+".tar.gz","w:gz")
#    tar.add("../analysis/fuzzTreeAnalysis.sh", arcname=basename+"/fuzzTreeAnalysis.sh")
#    tar.add("../analysis/initscript", arcname=basename+"/initscript")
#    tar.add("../analysis/jar/fuzzTreeAnalysis.jar", arcname=basename+"/jar/fuzzTreeAnalysis.jar")
#    tar.close()

#    os.chdir(current)

#@task
def rendering_server():
    '''Performs packaging of rendering server.'''
    current = os.getcwd()
    os.chdir('dist')

    basename="FuzzEdRendering-%s"%version
    tar = tarfile.open(basename+".tar.gz","w:gz")
    tar.add("../rendering/renderServer.py", arcname=basename+"/renderServer.py")
    tar.close()

    os.chdir(current)

@task
def all():
    '''Package all.'''
    web_server()
#   package_analysis_server()
#    rendering_server()
