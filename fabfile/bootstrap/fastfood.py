'''
This is fastfood.

It is intended as quick and unhealthy replacement for the Cuisine project.
It works nicely with Fabric, and concentrates only on package installation issues.
'''

from abc import ABCMeta, abstractmethod
import platform, os, subprocess, time

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
    def install(self, name):
        ''' Installs a package. The name is resolved from a registered mapping, if available.
            Otherwise it is used directly.
        '''

class HomebrewFastFood(FastFood):
    def install(self, name):
        super(HomebrewFastFood, self).run("brew install "+self.get_mapping(name))

    def tap(self, name):
        super(HomebrewFastFood, self).run("brew tap "+name)
        super(HomebrewFastFood, self).run("brew tap --repair")

class AptFastFood(FastFood):
    def install(self, name):
        super(AptFastFood, self).run("sudo apt-get install -y -qq "+self.get_mapping(name))

class PipFastFood(FastFood):
    def install(self, name):
        super(PipFastFood, self).run("sudo pip --default-timeout=100 install -q "+self.get_mapping(name))

class NpmFastFood(FastFood):
    def install(self, name):
        super(NpmFastFood, self).run("sudo npm install -g "+self.get_mapping(name))

# Initialize module variables
if platform.system() == "Darwin":
    system = HomebrewFastFood()
else:
    system = AptFastFood()
python = PipFastFood()
npm = NpmFastFood()


