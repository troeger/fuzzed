'''
This is Fastfood.

It is intended as quick and unhealthy partial replacement for the Cuisine project.
It works nicely with Fabric, and concentrates only on package installation issues.

Peter Troeger <peter@troeger.eu>
'''

from abc import ABCMeta, abstractmethod
import platform, os, subprocess, time

system, python, js = None, None, None                          # Force package manager index updates on startup

class FastFood():
    ''' Abstract base class for the FastFood functionality. It provides a set of generic functions
        needed by most of the package managers, which can be implemented soly based on the class library. '''
    __metaclass__ = ABCMeta 
    mappings = {}

    def set_mappings(self, mappings):
        ''' Defines a set of name mappings for the local platform.
            If the given key in the mappings dictionary is used as package name and cannot be found,
            the value is used instead.
            Returns nothing.
        '''
        self.mappings = mappings

    def get_mapping(self, name):
        ''' Returns the package mapping for the current platform, or the input value if not found. '''
        if name in self.mappings:
            return self.mappings[name]
        else:
            return name

    def run(self, args, print_output=True):
        ''' Run command and returns exit code. The command is given as array of command-line arguments,
            were the first argument is the executable.
        '''
        try:
            p = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            running = True
            while p.returncode == None:
                p.poll()
                if print_output:
                    stdout = ''.join(p.stdout.readlines()).strip()
                    stderr = ''.join(p.stderr.readlines()).strip()
                    if stdout:
                        print stdout
                    if stderr:
                        print '\033[1;31m'+stderr+'\033[1;m'.strip()
            return p.returncode
        except OSError as e:
            print "Error while running "+str(args)+": "+str(e)

    def check_output(self, args):
        ''' Runs the command and checks the output. The command is given as array of command-line arguments,
            were the first argument is the executable.
        '''
        try:
            output = subprocess.check_output(args)
            return output
        except OSError as e:
            print "Error while checking output of "+str(args)+": "+str(e)
            return None

    def which(self, program):
        ''' Checks if the program exists on the system, returns the full path or None. '''
        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

        fpath, fname = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file

        return None

    @abstractmethod
    def supported(self):
        ''' Checks if this package manager is supported on this system, and returns a boolean result. 
            In an ideal world, this would be an @abstractclassmethod, but this only works 
            from Python 3.3 and above.
        '''

    @abstractmethod
    def index_update(self):
        ''' Updates the package index for the package manager. Returns nothing.
        '''


    @abstractmethod
    def install(self, name, version=None):
        ''' Installs a package, returns nothing. 
            The name is resolved from a registered mapping, if available.
            Otherwise it is used directly. If the package is already installed in the given version,
            nothing will change in the system. 

            The version is given as string, were the first two characters must be one of the following:

            '>=': Install the package with at least this version number.
            '==': Install the package with exactly this version number.

            The two characters are followed by an arbitrary set of characters that expresses a version number in
            the particular package manager.

            If the version is not given, the packager manager decides which one to install. 
            Typically, this would be the most recent one.
        '''

class HomebrewFastFood(FastFood):
    def install(self, name, version=None):
        #TODO: Add version support
        assert(version==None)
        super(HomebrewFastFood, self).run("brew install "+self.get_mapping(name))
        # May have installed fresh package managers
        system, python, js = find_package_managers()

    def tap(self, name):
        super(HomebrewFastFood, self).run("brew tap "+name)
        super(HomebrewFastFood, self).run("brew tap --repair")

    def supported(self):
        return super(HomebrewFastFood, self).which("brew") != None

    def index_update(self):
        super(HomebrewFastFood, self).run("brew update")

homebrew = HomebrewFastFood()

class AptFastFood(FastFood):
    def install(self, name, version=None):
        #TODO: Add version support
        assert(version==None)
        super(AptFastFood, self).run("sudo apt-get install -y -qq "+self.get_mapping(name))
        # May have installed fresh package managers
        system, python, js = find_package_managers()

    def supported(self):
        return super(AptFastFood, self).which("apt-get") != None

    def index_update(self):
        super(AptFastFood, self).run("sudo apt-get update")

apt = AptFastFood()

class PipFastFood(FastFood):
    def install(self, name, version=None):
        if version and version.startswith('=='):
            super(PipFastFood, self).run("sudo pip --default-timeout=100 install -q '%s==%s'"%(self.get_mapping(name), version[2:]))
        elif version and version.startswith('>='):
            super(PipFastFood, self).run("sudo pip --default-timeout=100 install -q '%s>=%s'"%(self.get_mapping(name), version[2:]))
        else:
            super(PipFastFood, self).run("sudo pip --default-timeout=100 install -q "+self.get_mapping(name))

    def supported(self):
        return super(PipFastFood, self).which("pip") != None

    def index_update(self):
        pass

pip = PipFastFood()

class EasyInstallFastFood(FastFood):
    def install(self, name, version=None):
        if version and version.startswith('=='):
            super(EasyInstallFastFood, self).run("sudo easy_install '%s==%s'"%(self.get_mapping(name), version[2:]))
        elif version and version.startswith('>='):
            super(EasyInstallFastFood, self).run("sudo easy_install '%s>=%s'"%(self.get_mapping(name), version[2:]))
        else:
            super(EasyInstallFastFood, self).run("sudo easy_install "+self.get_mapping(name))

    def supported(self):
        return super(EasyInstallFastFood, self).which("easy_install") != None

    def index_update(self):
        pass

easy_install = EasyInstallFastFood()

class NpmFastFood(FastFood):
    def install(self, name, version=None):
        #TODO: Add version support
        assert(version==None)
        super(NpmFastFood, self).run("sudo npm install -g "+self.get_mapping(name))

    def supported(self):
        return super(NpmFastFood, self).which("npm") != None

    def index_update(self):
        pass

npm = NpmFastFood()

class MissingFastFood(FastFood):
    def install(self, name, version=None):
        raise Exception("Installation of package '%s' not possible, couldn't find any suitable package manager."%name)

    def supported(self):
        return True

    def index_update(self):
        pass

missing = MissingFastFood()

def find_package_managers():
    global system
    global python
    global js
    
    system_old = system
    python_old = python
    js_old = js

    # Determine system package manager
    if platform.system() == "Darwin":
        if homebrew.supported():
            system = homebrew
        else:
            system = missing
    else:
        if apt.supported():
            system = apt
        else:
            system = missing
    if system != system_old:
        system.index_update()

    # Set python package manager
    if pip.supported():
        python = pip
    elif easy_install.supported():
        python = easy_install
    else:
        python = missing
    if python != python_old:
        python.index_update()

    # Set JS package manager
    if npm.supported():
        js = npm
    else:
        js = missing
    if js != js_old:
        js.index_update()

    return system, python, js


#################################### Module initialization ####################################
system, python, js = find_package_managers()


