#!/usr/bin/env python
import os, json, pprint, sys, shutil, subprocess

from setuptools import setup
from distutils.command.build import build as _build
from distutils.command.clean import clean as _clean
from distutils.command.sdist import sdist as _sdist
# check FuzzEd/__init__.py for the project version number
from FuzzEd import __version__, util
from FuzzEd.setup_schemas import createFaultTreeSchema, createFuzzTreeSchema

IS_WINDOWS = os.name == 'nt'
FILE_EXTENSION = '.py' if IS_WINDOWS else ''
FILE_PREFIX = 'file:///' + os.getcwd() + '/' if IS_WINDOWS else '' 

def check_python_version():
    version_message = 'This Django project requires Python 2.7+'

    if sys.version_info.major < 2 or sys.version_info.major == 2 and sys.version_info.minor < 7:
        print version_message
        exit(-1)
    elif sys.version_info.major > 2:
        print(version_message)
        exit(-1)
check_python_version()

def check_java_version():
    output = subprocess.check_output('java -version', stderr=subprocess.STDOUT, shell=True)
    if (not 'version' in output) or (not '1.7' in output):
        raise Exception('We need at least Java 1.7 to build the analysis server. We found ' + output)

def build_schema_files():
    print "Generating XML schema files ..."
    createFaultTreeSchema("FuzzEd/static/xsd/faulttree.xsd")
    createFuzzTreeSchema("FuzzEd/static/xsd/fuzztree.xsd")

def build_xmlschema_wrapper():
    print 'Building XML schema wrappers ...'

    # Remove old binding files and generate new ones
    for file_name in ['xml_faulttree.py', 'xml_fuzztree.py', 'xml_analysis.py']:
        path_name = 'FuzzEd/models/%s' % file_name

        if os.path.exists(path_name):
            os.remove(path_name)
    if os.system('pyxbgen%s --binding-root=FuzzEd/models/ -u %sFuzzEd/static/xsd/analysis.xsd '
                 '-m xml_analysis -u %sFuzzEd/static/xsd/fuzztree.xsd -m xml_fuzztree -u %sFuzzEd/static/xsd/faulttree.xsd -m xml_faulttree'
                 % (FILE_EXTENSION, FILE_PREFIX, FILE_PREFIX, FILE_PREFIX,)) != 0:
        raise Exception('Execution of pyxbgen failed.\nTry "sudo setup.py test" for installing all dependencies.')

def build_naturaldocs():
    # Build natural docs in 'docs' subdirectory
    if not os.path.exists('docs'):
        os.mkdir('docs')
    if os.system('tools/NaturalDocs/NaturalDocs -i FuzzEd -o HTML docs -p docs') != 0:
        raise Exception('Execution of NaturalDocs compiler failed.')

def build_analysis_server():
    print 'Building analysis server JAR file ...'
    check_java_version()
    current = os.getcwd()
    os.chdir('analysis/jar')

    if os.system('ant clean') != 0:
        raise Exception('Execution of ANT failed. Is it installed?')

    if os.system('ant') != 0:
        raise Exception('Execution of ANT failed. Please check the previous output.')

    os.chdir(current)

def build_django_require():
    print 'Building compressed static files ...'
    # Use Django collectstatic, which triggers django-require optimization
    if os.system('./manage.py collectstatic -v3 --noinput') != 0:
        raise Exception('Execution of collectstatic failed. Please check the previous output.\n'
                        'Try "sudo setup.py test" for installing all dependencies.')

def notation_json_to_py(kind):
    # This code loads the JSON notation configuration and creates a Python representation
    # JSON inheritance is modeled with Python class inheritance
    jsonText=open("FuzzEd/static/notations/%s.json"%kind,"r").read()
    config=json.loads(jsonText)
    assert(config['kind']==kind)
    result=''
    # First take care of 'nodes' dictionary for this graph type, which relies on the inheritance concept
    # Go through all the graph nodes mentioned in the config file
    node_list=[]
    for node_name, node_configs in config['nodes'].iteritems():
        # Per node, go through all the configuration options
        base_class = '' 
        configs_as_attributes = ''
        for node_config_name, node_config_data in node_configs.iteritems():
            # If this configuration value is an inheritance flag, we have a base class
            if node_config_name == 'inherits':
                base_class = kind+"_"+node_config_data
            else:
                # for all other config options, just add them plainly
                if isinstance(node_config_data,unicode):
                    configs_as_attributes+="    %s = '%s'\n"%(node_config_name, node_config_data)
                else:
                    configs_as_attributes+="    %s = %s \n"%(node_config_name, node_config_data) 
        # Got the (maybe) base class and all the config options as class attributes, now adding them
        result += "\nclass %s_%s(%s):\n"%(kind, node_name, base_class)
        result += configs_as_attributes
        node_list.append(node_name)
    # Now comes the global information
    # The 'kind' attribute on root level of the JSON forms the class name
    result+="/nclass %s():/n"%kind
    # Add all attributes on the same root JSON level that are not node configurations
    for k,v in config.iteritems():
        if k != 'nodes':
            if isinstance(v,unicode):
                result+="    %s = '%s'\n"%(k,v)
            else:
                result+="    %s = %s\n"%(k,v)   
    # Add list of known nodes, but now as dict to class instances
    nodes_class_dict_entry=[]
    for node in node_list:
        nodes_class_dict_entry.append("'%s':%s_%s()"%(node, kind, node))
    result+="    nodes = {%s}"%(','.join(nodes_class_dict_entry))
    return result


def build_notations():
    print 'Building new Python version of notation configuration file ...'
    # write out Python versions as result
    with open('FuzzEd/models/notations.py', 'w') as out:
        old_stdout, sys.stdout = sys.stdout, out

        print '# DO NOT EDIT! This file is auto-generated by "setup.py build"\n'
        print notation_json_to_py('fuzztree')
        print notation_json_to_py('faulttree')
        print notation_json_to_py('rbd')
        print '\n# END OF GENERATED CONTENT'

        sys.stdout = old_stdout

# Our overloaded 'setup.py build' command
class build(_build):
    def run(self):
        _build.run(self)
        build_analysis_server()
        build_notations()
        build_schema_files()
        build_xmlschema_wrapper()

def clean_docs():
    os.system('rm -rf docs')

def clean_build_garbage():
    os.system('rm -rf FuzzEd.egg-info')
    os.system('rm -rf build')
    os.system('rm -rf dist')

def clean_pycs():
    # Clean all pyc files recursively
    for root, dirs, files in os.walk('.'):
        for name in files:
            if name.endswith('.pyc'):
                fullname = os.path.join(root, name)
                print 'Removing %s' % fullname
                os.remove(fullname)

# Our overloaded 'setup.py clean' command
class clean(_clean):
    def run(self):
        _clean.run(self)
        clean_docs()
        clean_pycs()
        clean_build_garbage()

# Our overloaded 'setup.py sdist' command
class sdist(_sdist):
    def run(self):
        build_naturaldocs()
        build_django_require()
        _sdist.run(self)

setup(
    name = 'FuzzEd',
    version = __version__,
    packages = ['FuzzEd'],
    include_package_data = True,
    cmdclass={
        'build': build,
        'clean': clean,
        'sdist': sdist
    },
    maintainer = 'Peter Troeger',
    maintainer_email = 'peter.troeger@hpi.uni-potsdam.de',
	url = 'https://bitbucket.org/troeger/fuzztrees'
)
