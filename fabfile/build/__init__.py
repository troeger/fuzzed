
@task
def backends():
    '''Builds configuration and analysis server with CMAKE / C++11 compiler.'''
    print 'Building backend servers ...'
    current = os.getcwd()
    os.chdir('backends')
    if os.path.isfile("CMakeCache.txt"):
        os.system("rm CMakeCache.txt")
    if platform.system() == "Darwin":
        os.system("cmake -D CMAKE_C_COMPILER=/usr/local/bin/gcc-4.9 -D CMAKE_CXX_COMPILER=/usr/local/bin/g++-4.9 .")
    else:
        os.system("cmake .")
    os.system('make all')
    os.chdir(current)


