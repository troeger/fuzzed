import os
from fabric.api import task

@task
def docs():
    '''Cleans generated source code documentation.'''     
    os.system('rm -rf docs')

@task
def build_garbage():
    '''Cleans build files, including packages in /dist.'''     
    os.system('rm -rf build')
    os.system('rm -rf dist')
    os.system('rm -rf FuzzEd/static-release')

@task
def pycs():
    '''Cleans .pyc files recursively.'''     
    # Clean all pyc files recursively
    for root, dirs, files in os.walk('.'):
        for name in files:
            if name.endswith('.pyc'):
                fullname = os.path.join(root, name)
                os.remove(fullname)

@task
def all():
    '''Cleans all.'''    
    docs()
    build_garbage()
    pycs()

