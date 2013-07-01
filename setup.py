#!/usr/bin/env python
import os, json, pprint, sys, shutil, subprocess
from xml.dom.minidom import parse as parseXml

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

def svg2pgf_shape(name, filename):
    #TODO: Get size from DOM tree, use the values
    #      Add rectangle and circle paths
    #      Build a command for some test output
    result = '''
        \\pgfdeclareshape{%s}{
            \\anchor{center}{\pgfpoint{18}{18}}
            \\anchor{north}{\pgfpoint{18}{36}}
            \\anchor{south}{\pgfpoint{18}{0}}
            \\anchor{west}{\pgfpoint{0}{18}}
            \\anchor{east}{\pgfpoint{36}{18}}
            \\foregroundpath{
                \\pgfsetlinewidth{1.4}
'''%name
    xml = parseXml(filename)
    # add all SVG paths
    pathCommands = xml.getElementsByTagName('path')
    for p in pathCommands:
        result += "                \\pgfpathsvg{%s}\n"%p.attributes['d'].value
    result += '                \\pgfusepath{stroke} } }'
    return result

def build_pgf_shape_lib(startdir='FuzzEd/static/img', covered=[]):
    ''' 
        Build static LaTex representation for our graphical symbols as TiKZ shapes.
        Some SVGs occur multiple times in subdirectories, so we track the already
        converted ones. 
    '''
    result = ''
    for root, dirs, files in os.walk(startdir):
        for d in dirs:
            result += build_pgf_shape_lib(root+d,covered)
        for f in files:
            if f.endswith('.svg') and f not in covered:
                result += svg2pgf_shape(f, root+os.sep+f)
                covered.append(f)
    return result

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

def build_notations():
    notations_dir = 'FuzzEd/static/notations/'
    file_list = os.listdir(notations_dir)
    notations = []

    for file_path in [os.path.join(notations_dir, file_name) for file_name in file_list]:
        if os.path.isfile(file_path) and file_path.endswith('.json'):

            with open(file_path) as handle:
                notations.append(json.loads(handle.read()))
    resolve_inheritance(notations)

    out=open('FuzzEd/models/notations.py', 'w')
    out.write('# DO NOT EDIT! This file is auto-generated by "setup.py build"\n')
    out.write('notations = ')
    pprint.pprint(notations, out)
    out.write('\nby_kind = {notation[\'kind\']: notation for notation in notations}\n')
    out.write('choices = ')
    pprint.pprint(generate_choices(notations), out)
    out.write('\nnode_choices = ')
    pprint.pprint(generate_node_choices(notations), out)
    out.write('\n# END OF GENERATED CONTENT')

def generate_choices(notations):
    return [(notation['kind'], notation['name']) for notation in notations]

def generate_node_choices(notations):
    node_choices = []

    for notation in notations:
        nodes = notation['nodes']
        node_category = (notation['name'],)
        node_category_choices = ()

        for node_kind, node in nodes.items():
            node_category_choices += ((node_kind, node['nodeDisplayName']),)

        node_category += (node_category_choices,)
        node_choices.append(node_category)

    return node_choices

def resolve_inheritance(notations):
    for notation in notations:
        nodes = notation['nodes']
        node_cache = {}

        for node_name, node in nodes.items():
            nodes[node_name] = inherit(node_name, node, nodes, node_cache)

def inherit(node_name, node, nodes, node_cache):
    inherits_from = node.get('inherits')

    if not inherits_from:
        node_cache[node_name] = node
        return node

    elif inherits_from not in node_cache:
        inherit(inherits_from, nodes[inherits_from], nodes, node_cache)

    resolved = util.extend({}, node_cache[inherits_from], node, deep=True)
    node_cache[node_name] = resolved

    return resolved

# Our overloaded 'setup.py build' command
class build(_build):
    def run(self):
        _build.run(self)
#        build_analysis_server()
#        build_notations()
#        build_schema_files()
#        build_xmlschema_wrapper()
        build_pgf_shape_lib()

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
