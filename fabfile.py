import os, json, pprint, shutil, tarfile, sys, platform, subprocess
from contextlib import contextmanager
from xml.dom.minidom import parse as parseXml
# check FuzzEd/__init__.py for the project version number
from FuzzEd import __version__, util, settings
from FuzzEd.setup_schemas import createFaultTreeSchema, createFuzzTreeSchema

from fabric.api import run, local, task

sys.path.append('tools')    # not needed when cuisine comes from PyPI
import cuisine
cuisine.mode_local()

def svg2pgf_shape(filename):
    '''
        Convert given SVG file to TiKZ code.
    '''
    xml = parseXml(filename)
    # determine size of the picture from SVG source
    svg = xml.getElementsByTagName('svg')[0]
    name = svg.attributes['id'].value
    height = int(svg.attributes['height'].value)
    width = int(svg.attributes['width'].value)
    # Define shape anchors, based on image size
    # We need double backslashes since the output is Python again
    # The SVG coordinate system is mirrored on the horizon axis, so we add a rotation command and a positional compensation
    result = '''
\\\\pgfdeclareshape{%(name)s}{
    \\\\anchor{center}{\pgfpoint{%(halfwidth)u}{%(halfheight)u}}
    \\\\anchor{north}{\pgfpoint{%(halfwidth)u}{%(height)u}}
    \\\\anchor{south}{\pgfpoint{%(halfwidth)u}{0}}
    \\\\anchor{west}{\pgfpoint{0}{%(halfheight)u}}
    \\\\anchor{east}{\pgfpoint{%(width)u}{%(halfheight)u}}
    \\\\foregroundpath{
        \\\\pgfsetlinewidth{1.4}
        \\\\pgftransformshift{\pgfpoint{%(width)u}{%(height)u}}
        \\\\pgftransformrotate{180} 
        \\\\pgfsetfillcolor{white}
'''%{'name':name, 'height':height, 'halfheight':height/2, 'width':width, 'halfwidth':width/2}
    # add all SVG path
    pathCommands = xml.getElementsByTagName('path')
    for p in pathCommands:
        # The path may have styling. We ignore everything but dashing.
        if p.attributes.has_key('style'):
            if 'stroke-dasharray' in p.attributes['style'].value:
                # http://stuff.mit.edu/afs/athena/contrib/tex-contrib/beamer/pgf-1.01/doc/generic/pgf/version-for-tex4ht/en/pgfmanualse23.html
                result += "        \\\\pgfsetdash{{4.2}{1.4}}{0}\n"
        # Add the SVG path
        result +="        \\\\pgfpathsvg{%s}\n"%p.attributes['d'].value
    # add all SVG rectangle definitions
    # Add usepath after each rectangle, in order to get overlayed filled rects correctly generated
    rectCommands = xml.getElementsByTagName('rect')
    for r in rectCommands:
        rheight = float(r.attributes['height'].value)
        rwidth = float(r.attributes['width'].value)
        x = float(r.attributes['x'].value)
        y = float(r.attributes['y'].value)
        result += "        \\\\pgfrect{\pgfpoint{%f}{%f}}{\pgfpoint{%f}{%f}}\n\\\\pgfusepath{stroke, fill}\n"%(x, y, rwidth, rheight)
    # add all SVG circle definitions
    circleCommands = xml.getElementsByTagName('circle')
    for c in circleCommands:
        x = float(c.attributes['cx'].value)
        y = float(c.attributes['cy'].value)
        radius = float(c.attributes['r'].value)
        result += "        \\\\pgfcircle{\pgfpoint{%f}{%f}}{%f}\n\\\\pgfusepath{stroke, fill}\n"%(x,y,radius)
    # finalize TiKZ shape definition
    result += '        \\\\pgfusepath{stroke}\n}}'
    return result

def build_shape_lib_recursive(startdir='FuzzEd/static/img', covered=[]):
    ''' 
        Build static LaTex representation for our graphical symbols as TiKZ shapes.
        Some SVGs occur multiple times in subdirectories, so we track the already
        converted ones. 
    '''
    result = ''
    for root, dirs, files in os.walk(startdir):
        for d in dirs:
            result += build_shape_lib_recursive(root+d,covered)
        for f in files:
            if f.endswith('.svg') and f not in covered:
                try:
                    result += svg2pgf_shape(root+os.sep+f)
                    covered.append(f)
                    print "Converting %s to TiKZ shape ..."%f
                except Exception, e:
                    print "Error on parsing, ignoring %s ..."%f
                    print e
    return result

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

@task
def clean_docs():
    '''Cleans generated source code documentation.'''     
    os.system('rm -rf docs')

@task
def clean_build_garbage():
    '''Cleans build files, including packages in /dist.'''     
    os.system('rm -rf build')
    os.system('rm -rf dist')
    os.system('rm -rf FuzzEd/static-release')

@task
def clean_pycs():
    '''Cleans .pyc files recursively.'''     
    # Clean all pyc files recursively
    for root, dirs, files in os.walk('.'):
        for name in files:
            if name.endswith('.pyc'):
                fullname = os.path.join(root, name)
                os.remove(fullname)

@task
def clean():
    '''Cleans all.'''    
    clean_docs()
    clean_build_garbage()
    clean_pycs()

@task
def build_shapes():
    '''Builds TiKZ shape library needed for Latex export / rendedering server.'''
    print "Generating TiKZ shape library ..."
    f=open("FuzzEd/models/node_rendering.py","w")
    f.write("# Auto-generated by 'setup.py build', do not change !\n")
    f.write("tikz_shapes='''")
    f.write("\n%% Start of shape library. This part remains the same for all graph exports.")
    f.write(build_shape_lib_recursive())
    f.write("\n%% End of shape library. This part below is unique for all graph exports.\n")    
    f.write("'''")
    f.close()

@task
def build_notations():
    '''Builds Python equivalents of notation JSON files.'''
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

def build_xmlschema_wrappers():
    print 'Building XML schema wrappers ...'

    IS_WINDOWS = os.name == 'nt'
    FILE_EXTENSION = '.py' if IS_WINDOWS else ''
    FILE_PREFIX = 'file:///' + os.getcwd() + '/' if IS_WINDOWS else '' 

    # Remove old binding files and generate new ones
    for file_name in ['xml_faulttree.py', 'xml_fuzztree.py', 'xml_analysis.py']:
        path_name = 'FuzzEd/models/%s' % file_name

        if os.path.exists(path_name):
            os.remove(path_name)
    if os.system('pyxbgen%s --binding-root=FuzzEd/models/ -u %sFuzzEd/static/xsd/analysis.xsd '
                 '-m xml_analysis -u %sFuzzEd/static/xsd/fuzztree.xsd -m xml_fuzztree -u %sFuzzEd/static/xsd/faulttree.xsd -m xml_faulttree'
                 % (FILE_EXTENSION, FILE_PREFIX, FILE_PREFIX, FILE_PREFIX,)) != 0:
        raise Exception('Execution of pyxbgen failed.\nTry "sudo setup.py test" for installing all dependencies.')

@task
def build_xmlschemas():
    '''Builds XML schema files and according Python wrappers.'''
    print "Generating XML schema files ..."
    createFaultTreeSchema("FuzzEd/static/xsd/faulttree.xsd")
    createFuzzTreeSchema("FuzzEd/static/xsd/fuzztree.xsd")
    build_xmlschema_wrappers()

@task
def build_naturaldocs():
    '''Builds source code documentation in /docs.'''
    # Build natural docs in 'docs' subdirectory
    if not os.path.exists('docs'):
        os.mkdir('docs')
    if os.system('tools/NaturalDocs/NaturalDocs -i FuzzEd -i analysis -i rendering -xi FuzzEd/static/lib -o HTML docs -p docs ') != 0:
        raise Exception('Execution of NaturalDocs compiler failed.')

@task
def build_analysis_server():
    '''Builds analysis server.'''
    print 'Building analysis server JAR file ...'
    current = os.getcwd()
    os.chdir('analysis/jar')

    if os.system('ant clean') != 0:
        raise Exception('Execution of ANT failed. Is it installed?')

    if os.system('ant') != 0:
        raise Exception('Execution of ANT failed. Please check the previous output.')

    os.chdir(current)

@task
def build():
    '''Builds all.'''
    build_shapes()
    build_xmlschemas()
    build_naturaldocs()
    build_analysis_server()
    build_notations()

@task
def package_web_server():
    '''Performs packaging of web server. Assumes successful build.'''
    with created_dir("dist"):
        exclusion_suffix=[".pyc", ".sqlite"]
        exclusion_files =[
            "../FuzzEd/setup_schemas.py",
            "../FuzzEd/settings_production.py"
        ]
        exclusion_dirs =[
            "../FuzzEd/static/",
            "../FuzzEd/fixtures/"
        ]
        inclusions = [
            ["../manage.py", "manage.py"],
            ["../rendering/__init__.py", "rendering/__init__.py"],
            ["../rendering/renderClient.py", "rendering/renderClient.py"],
            ["../FuzzEd/settings_production.py", "FuzzEd/settings_local.py"],
            ["../FuzzEd", "FuzzEd"],
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

        basename="FuzzEd-%s"%__version__
        tar = tarfile.open(basename+".tar.gz","w:gz")
        for src, dest in inclusions:
            tar.add(src, arcname=basename+"/"+dest, exclude=add_filter)
        tar.close()

@task
def package_analysis_server():
    '''Performs packaging of analysis server. Assumes successful build.'''
    current = os.getcwd()
    os.chdir('dist')

    basename="FuzzEdAnalysis-%s"%__version__
    tar = tarfile.open(basename+".tar.gz","w:gz")
    tar.add("../analysis/fuzzTreeAnalysis.sh", arcname=basename+"/fuzzTreeAnalysis.sh")
    tar.add("../analysis/initscript", arcname=basename+"/initscript")
    tar.add("../analysis/jar/fuzzTreeAnalysis.jar", arcname=basename+"/jar/fuzzTreeAnalysis.jar")
    tar.close()

    os.chdir(current)

@task
def package_rendering_server():
    '''Performs packaging of rendering server.'''
    current = os.getcwd()
    os.chdir('dist')

    basename="FuzzEdRendering-%s"%__version__
    tar = tarfile.open(basename+".tar.gz","w:gz")
    tar.add("../rendering/renderServer.py", arcname=basename+"/renderServer.py")
    tar.close()

    os.chdir(current)

@task
def package():
    '''Package all. Assumes successful build.'''
    print 'Building compressed static files ...'
    # Use Django collectstatic, which triggers django-require optimization
    if os.system('./manage.py collectstatic -v3 --noinput') != 0:
        raise Exception('Execution of collectstatic failed. Please check the previous output.\n'
                        'Try "sudo setup.py test" for installing all dependencies.')
    package_web_server()
    package_analysis_server()
    package_rendering_server()

@task
def fixture_save(fname=None):
    '''Creates a test fixture from the current database in ./FuzzEd/fixtures/'''
    if fname==None:
        print "Usage: fab fixture_save:<filename>"
        return
    testaccount = {"model": "auth.user", "pk": 2,
        "fields": {
            "username" : "testadmin",
            "password" : "pbkdf2_sha256$10000$JNt1EZn2g72p$vX3UFh7g4mPa313pWW4lf4YxkUhL534V8/kxFaQ1XvM="
        }
    }
    jsontext = subprocess.check_output(['./manage.py','dumpdata','FuzzEd.node','FuzzEd.edge','FuzzEd.graph','FuzzEd.property'])
    data = json.loads(jsontext)
    data.append(testaccount)
    output=open("./FuzzEd/fixtures/"+fname,"w")
    output.write(json.dumps(data, indent=4))
    output.close()

@task
def fixture_load(fname=None):
    '''Loads the database with a test fixture from ./FuzzEd/fixtures/'''
    if fname==None:
        print "Usage: fab fixture_load:<filename>"
        return
    os.system('./manage.py loaddata ./FuzzEd/fixtures/'+fname)

@task
def reset_db():
    '''Resets the database without further questions.'''
    # We don't want to do that on the production database. Ever.
    assert(settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3')
    os.system('./manage.py syncdb --noinput --no-initial-data --migrate')

@task
def run_tests():
    '''Runs all the tests.'''
    os.system('./manage.py test FuzzEd')

@task 
def bootstrap_dev():
    '''Installs all software needed to make the machine a development machine.'''
    print "Installing Python packages..."
    for package in ["django", "south", "openid2rp", "django-require", "pyxb", "beanstalkc", "django-less"]:
        print cuisine.python_package_ensure(package)        
    print "Installing native packages ..."
    print cuisine.package_ensure("beanstalkd")
    if platform.system() != 'Darwin':
        print cuisine.package_ensure("texlive")
        print cuisine.package_ensure("openjdk-7-jdk")
        print cuisine.package_ensure("node-less")  # only in Debian unstable
	print cuisine.package_ensure("ant-gcj")
    else:
        # check Java version
        output = cuisine.run('javac -version')
        if not '1.7' in output:
            raise Exception('We need at least JDK 7 to build the analysis server. We found ' + output)
        # check if latex is installed
        output = cuisine.run('dvips')
        if 'command not found' in output:
            raise Exception('We need a working Latex for the rendering server. Please install it manually.')
        # Install LESS compiler via NPM, since no brew exists for that
        cuisine.package_ensure("npm")
        output = cuisine.run('lessc')
        if 'command not found' in output:
            cuisine.sudo("npm install less --global")

@task 
def bootstrap_web():
    '''Installs all software needed to make the machine a web server machine.'''
    for package in ["django", "south", "openid2rp", "pyxb", "beanstalkc", "django-less"]:
        cuisine.python_package_ensure(package)        
    cuisine.package_ensure("apache2")
    cuisine.package_ensure("libapache2-mod-wsgi")
    cuisine.package_ensure("postgresql")
    cuisine.package_ensure("python-psycopg2")
    #TODO: Prepare database
    #TODO: Prepare Apache config
    #TODO: Ask for IP of Beanstalk server

@task 
def bootstrap_backend():
    '''Installs all software needed to make the machine a backend machine.'''
    for package in ["pyxb", "beanstalkc"]:
        cuisine.python_package_ensure(package)        
    cuisine.package_ensure("beanstalkd")
    if platform.system() != 'Darwin':
        cuisine.package_ensure("texlive")
        cuisine.package_ensure("openjdk-7-jre")
    else:
        # check Java version
        output = subprocess.check_output('java -version', stderr=subprocess.STDOUT, shell=True)
        if (not 'version' in output) or (not '1.7' in output):
            raise Exception('We need at least JDK 7 to build the analysis server. Please install it manually.')
        # check if latex is installed
        if not cmd_exists("latex"):
            raise Exception('We need a working Latex for the rendering server. Please install it manually.')
    #TODO: Ask if Beanstalkd should be installed here

#TODO: Introduce task to start the dev server with one fabric task
#    - Checks if initial building or SQLite creation is needed
#    - Starts the backend servers
#    - Starts the django web server

#TODO: Introduce DEPLOY task:
#    - Push the packaged release on the server(s).
#    - Trigger cuisine on production machine to update the software installation.
#    - Restart the web server / analysis server / rendering server.
#    - Extra fab tasks for web server / rendering server / analysis server deployment.
#    - Check for correct installation of init scripts.
#
#    Installation of production backend server
#    -----------------------------------------
#    > sudo puppet apply install/prod_backend.pp
#    > tar xvfz FuzzEdAnalysis-x.x.x.tar.gz /home/fuzztrees
#    > ln -s /home/fuzztrees/FuzzEdAnalysis-x.x.x /home/fuzztrees/analysis 
#    > ln -s /home/fuzztrees/analysis/initscript /etc/init.d/fuzzTreesAnalysis
#    > tar xvfz FuzzEdRendering-x.x.x.tar.gz /home/fuzztrees
#    > ln -s /home/fuzztrees/FuzzEdRendering-x.x.x /home/fuzztrees/rendering 
#    > ln -s /home/fuzztrees/rendering/initscript /etc/init.d/fuzzTreesRendering##
#
#    Install new release on production web server
#    --------------------------------------------
#    > sudo puppet apply install/prod_web.pp
#    > tar xvfz FuzzEd-x.x.x.tar.gz /var/www/fuzztrees.net/
#    > ln -s /var/www/fuzztrees.net/FuzzEd-x.x.x /var/www/fuzztrees.net/www
#    > service apache2 restart
#
#TODO: test how well this works with Vagrant for Linux dev machines


