'''
This is Fastfood.

It is intended as quick and unhealthy partial replacement for the Cuisine project.
It works nicely with Fabric, and concentrates only on package installation issues.

Peter Troeger <peter@troeger.eu>
'''

#TODO: Alles auf Python Logging umstellen
#      Readme schreiben, welches das Autodetect-Konzept erklaert
#      Nur beim Finden neuer Package-Manager Meldung ausgeben (system_old)
#      Readme schreiben
#      Ab auf Github und PyPI

from abc import ABCMeta, abstractmethod
import platform, os, subprocess, time, sys

class FastFood():
    ''' Abstract base class for the FastFood functionality. It provides a set of generic functions
        needed by most of the package managers, which can be implemented soly based on the class library. '''
    __metaclass__ = ABCMeta 
    mappings = {}               # Mappings registered for this package manager
    index_updated = False       # Was the index already updated ?

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
                        sys.stdout.flush()
                    if stderr:
                        print '\033[1;31m'+stderr+'\033[1;m'.strip()
                        sys.stderr.flush()
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

    def pre_install(self):
        ''' Call by the subclass package manager implementation before the actual
            implementation process.
        '''
        if not self.index_updated:
            self.index_update()
            self.index_updated = True

    def post_install(self):
        ''' Called by the subclass package manager implementation after the actual
            installation procedure.
        '''
        # Update detected package managers, in case one of them was installed
        find_package_managers()

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

            If the version is not given, the packager manager decides if and what is installed. 
        '''

class HomebrewFastFood(FastFood):
    def install(self, name, version=None):
        super(HomebrewFastFood, self).pre_install()
        #TODO: Add version support
        assert(version==None)
        super(HomebrewFastFood, self).run("brew install "+self.get_mapping(name))
        super(HomebrewFastFood, self).post_install()

    def tap(self, name):
        super(HomebrewFastFood, self).run("brew tap "+name)
        super(HomebrewFastFood, self).run("brew tap --repair")

    def supported(self):
        return super(HomebrewFastFood, self).which("brew") != None

    def index_update(self):
        super(HomebrewFastFood, self).run("brew update")

_homebrew = HomebrewFastFood()


class AptFastFood(FastFood):
    def install(self, name, version=None):
        super(AptFastFood, self).pre_install()
        #TODO: Add version support
        assert(version==None)
        super(AptFastFood, self).run("sudo apt-get install -y -qq "+self.get_mapping(name))
        super(AptFastFood, self).post_install()

    def supported(self):
        return super(AptFastFood, self).which("apt-get") != None

    def index_update(self):
        super(AptFastFood, self).run("sudo apt-get update")

_apt = AptFastFood()


class PipFastFood(FastFood):
    def install(self, name, version=None):
        super(PipFastFood, self).pre_install()
        if version and version.startswith('=='):
            super(PipFastFood, self).run("sudo pip --default-timeout=100 install -q '%s==%s'"%(self.get_mapping(name), version[2:]))
        elif version and version.startswith('>='):
            super(PipFastFood, self).run("sudo pip --default-timeout=100 install -q '%s>=%s'"%(self.get_mapping(name), version[2:]))
        else:
            super(PipFastFood, self).run("sudo pip --default-timeout=100 install -q "+self.get_mapping(name))
        super(PipFastFood, self).post_install()

    def supported(self):
        return super(PipFastFood, self).which("pip") != None

    def index_update(self):
        pass

_pip = PipFastFood()


class EasyInstallFastFood(FastFood):
    def install(self, name, version=None):
        super(EasyInstallFastFood, self).pre_install()
        if version and version.startswith('=='):
            super(EasyInstallFastFood, self).run("sudo easy_install '%s==%s'"%(self.get_mapping(name), version[2:]))
        elif version and version.startswith('>='):
            super(EasyInstallFastFood, self).run("sudo easy_install '%s>=%s'"%(self.get_mapping(name), version[2:]))
        else:
            super(EasyInstallFastFood, self).run("sudo easy_install "+self.get_mapping(name))
        super(EasyInstallFastFood, self).post_install()

    def supported(self):
        return super(EasyInstallFastFood, self).which("easy_install") != None

    def index_update(self):
        pass

_easy_install = EasyInstallFastFood()


class NpmFastFood(FastFood):
    def install(self, name, version=None):
        super(NpmFastFood, self).pre_install()        
        #TODO: Add version support
        assert(version==None)
        super(NpmFastFood, self).run("sudo npm install -g "+self.get_mapping(name))
        super(NpmFastFood, self).post_install()        

    def supported(self):
        return super(NpmFastFood, self).which("npm") != None

    def index_update(self):
        pass

_npm = NpmFastFood()


class MissingFastFood(FastFood):
    def install(self, name, version=None):
        raise Exception("Installation of package '%s' not possible, couldn't find any suitable package manager."%name)

    def supported(self):
        return True

    def index_update(self):
        pass

_missing = MissingFastFood()

system, python, js = None, None, None
    
def find_package_managers():    
    ''' Checks the system state by the help of the package manager supported()
        methods, and sets the global access variables system, python, and js.
    '''
    global system, python, js, _homebrew, _apt, _pip, _easy_install, _npm, _missing

    # Determine system package manager
    if platform.system() == "Darwin":
        if _homebrew.supported():
            system = _homebrew
        else:
            system = _missing
    else:
        if _apt.supported():
            system = _apt
        else:
            system = _missing

    # Set python package manager
    if _pip.supported():
        python = _pip
    elif _easy_install.supported():
        python = _easy_install
    else:
        python = _missing

    # Set JS package manager
    if _npm.supported():
        js = _npm
    else:
        js = _missing

############################### Module initialization ###############################
find_package_managers()


