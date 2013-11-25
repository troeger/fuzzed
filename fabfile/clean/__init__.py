import os
from fabric.api import task

@task
def docs():
    '''Cleans generated source code documentation.'''     
    os.system('rm -rf docs')

@task 
def gen_files():
    '''Cleans generated files produced by some of the build.all tasks.'''
    os.system('rm FuzzEd/models/xml_*.py')
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
def cmake_dirs():
    '''Remove temporary stuff created by CMake.'''
    for root, dirs, files in os.walk('backends'):
        if "Makefile" in files:
            olddir = os.getcwd()
            os.chdir(root)
            os.system("make clean")
            os.chdir(olddir)
        for name in dirs:
            if name == "CMakeFiles":
                fullname = os.path.join(root, name)
                os.system("rm -r "+fullname)
        for name in files:
            if name in ["CMakeCache.txt"]:
                fullname = os.path.join(root, name)
                os.system("rm -r "+fullname)

@task
def all():
    '''Cleans all.'''    
    docs()
    gen_files()
    pycs()
    cmake_dirs()

