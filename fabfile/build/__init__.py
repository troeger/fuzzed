import platform
import os
import json
import pprint
from xml.dom.minidom import parse as parseXml

from fabric.api import task

from setup_schemas import createFaultTreeSchema, createFuzzTreeSchema
from setup_settings import createDjangoSettings, createBackendSettings
from FuzzEd import util

# check FuzzEd/__init__.py for the project version number
# from FuzzEd import __version__, util, settings


XSD_PY_FILE_MAP = {
    'backendResult':       'xml_backend',
    'fuzztree':            'xml_fuzztree',
    'faulttree':           'xml_faulttree',
    'commonTypes':         'xml_common',
    'configurations':      'xml_configurations'
}

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
        notation[u'edges'] = notation.get(u'edges', {})
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

def generate_graphml_keys(notations):
    '''
        Derive the GraphML preamble from our notations file. This is cool,
        because our GraphML import / export magically matches to the notations file.

        GraphML allows to define extensions as part of the document, by having
        <key> elements that describe the extensions. Later <data> elements
        can refer to these keys.

        Our GraphML export behaves nicely and always adds this preamble, so that
        other GraphML tools can render the values nicely. For this reason,
        the 'graphml_keys' list is generated. It is just an ugly collection of XML
        definitions, which means that Marcus violates his own understand of 
        beautiful code ... 

        Our GraphML import does not rely on the existence of this preamble, but
        simply wants to know if a given GraphML <data> element refers to a valid key. 
        For this reason, the 'graphml_graph_data' and 'graphml_node_data' list is generated.
        It tells the import code if a graph / node element in the input XML is allowed
        to have a particulary named data element.
    '''
    graphml_keys = {}
    graphml_graph_data = {}
    graphml_node_data = {}

    def generate_key_xml(name, kind, default, for_what='node'):
        return \
            '        <key id="%s" for="%s" attr.name="%s" attr.type="%s">\n' \
            '            <default>%s</default>\n' \
            '        </key>' % (name, for_what, name, kind, default,)


    for notation in notations:
        notation_kind = notation['kind']
        graphml_graph_data[notation_kind] = set(['kind'])
        graphml_node_data[notation_kind] = set(['id','kind','x','y'])
        properties    = set()
        all_keys      = [
            generate_key_xml('id', 'string', '0'),
            generate_key_xml('kind', 'string', 'node'),
            generate_key_xml('x', 'long', '0'),
            generate_key_xml('y', 'long', '0'),
            generate_key_xml('kind', 'string', 'faulttree', 'graph')
        ]

        for node_kind, node in notation['nodes'].items():
            for property_name, propertie in node.get('properties', {}).items():
                if property_name in properties:
                    continue
                else:
                    properties.add(property_name)

                property_default = propertie.get('default', '')
                property_kind    = propertie['kind']
                key              = None
                keys             = None

                if property_kind in {'text', 'textfield'}:
                    key = generate_key_xml(property_name, 'string', property_default if propertie != 'name' else 'Node')
                    graphml_node_data[notation_kind].add(property_name)
                elif property_kind == 'compound':
                    parts_index    = property_default[0]
                    compound_parts = propertie['parts']

                    keys = [
                        generate_key_xml(property_name,          'string', property_default[1]),
                        generate_key_xml(property_name + 'Kind', 'string', compound_parts[parts_index]['partName']),
                    ]
                    graphml_node_data[notation_kind].add(property_name)
                elif property_kind == 'bool':
                    key = generate_key_xml(property_name, 'boolean', 'true' if property_default else 'false')
                    graphml_node_data[notation_kind].add(property_name)
                elif property_kind == 'choice':
                    index = propertie['values'].index(property_default)
                    property_default = property_default[index]
                    key = generate_key_xml(property_name, 'string', property_default)
                    graphml_node_data[notation_kind].add(property_name)
                elif property_kind == 'epsilon':
                    keys = [
                        generate_key_xml(property_name,             'double', property_default[0]),
                        generate_key_xml(property_name + 'Epsilon', 'double', property_default[1])
                    ]
                    graphml_node_data[notation_kind].add(property_name)
                elif property_kind in {'numeric', 'range'}:
                    kind = 'long' if propertie.get('step', 1) == 1 else 'double'

                    if property_name != 'missionTime':
                        key = generate_key_xml(property_name, kind, property_default)
                        graphml_node_data[notation_kind].add(property_name)
                    else:
                        key = generate_key_xml(property_name, kind, property_default, 'graph')
                        graphml_graph_data[notation_kind].add(property_name)
                elif property_kind == 'transfer':
                    key = generate_key_xml(property_name, 'string', '')
                    graphml_node_data[notation_kind].add(property_name)

                if key is not None:
                    all_keys.append(key)
                else:
                    all_keys.extend(keys)

        graphml_keys[notation_kind] = '\n'.join(all_keys)

    return graphml_keys, graphml_graph_data, graphml_node_data

@task
def shapes():
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
def notations():
    '''Builds Python equivalents of notation JSON files.'''
    notations_dir = 'FuzzEd/static/notations/'
    file_list = os.listdir(notations_dir)
    notations = []

    for file_path in [os.path.join(notations_dir, file_name) for file_name in file_list]:
        if os.path.isfile(file_path) and file_path.endswith('.json'):

            with open(file_path) as handle:
                notations.append(json.loads(handle.read()))
    resolve_inheritance(notations)


    with open('FuzzEd/models/notations.py', 'w') as out:
        out.write('# DO NOT EDIT! This file is auto-generated by "setup.py build"\n')
        out.write('notations = ')
        pprint.pprint(notations, out)
        out.write('\nby_kind = {notation[\'kind\']: notation for notation in notations}\n')
        out.write('choices = ')
        pprint.pprint(generate_choices(notations), out)
        out.write('\nnode_choices = ')
        pprint.pprint(generate_node_choices(notations), out)
        key_xml, graph_data, node_data = generate_graphml_keys(notations)
        out.write('\ngraphml_keys = ')
        pprint.pprint(key_xml, out)
        out.write('\ngraphml_graph_data = ')
        pprint.pprint(graph_data, out)
        out.write('\ngraphml_node_data = ')
        pprint.pprint(node_data, out)
        out.write('\n# END OF GENERATED CONTENT')

def build_xmlschema_wrappers():
    print 'Building XML schema wrappers ...'

    IS_WINDOWS     = os.name == 'nt'
    FILE_EXTENSION = '.py' if IS_WINDOWS else ''
    FILE_PREFIX    = ('file:///' + os.getcwd() + '/' if IS_WINDOWS else '') + 'FuzzEd/static/xsd/'
    BASE_PATH      = 'FuzzEd/models'

    # Remove old binding files and generate new ones
    for binding in XSD_PY_FILE_MAP.values():
        path = '%s/%s.py' % (BASE_PATH, binding,)
        if os.path.exists(path):
            os.remove(path)

    BINDINGS = ' '.join(['-u %(path)s%(xsd)s.xsd -m %(py)s' % {
        'path': FILE_PREFIX,
        'xsd':  xsd,
        'py':   py
    } for xsd, py in XSD_PY_FILE_MAP.items()])

    # generate new bindings
    if os.system('pyxbgen%(extension)s --binding-root=%(root)s %(bindings)s' % {
        'extension': FILE_EXTENSION,
        'root':      BASE_PATH,
        'bindings':  BINDINGS
    }) != 0:
        raise Exception('Execution of pyxbgen failed.')

@task
def xmlschemas():
    '''Builds XML schema files and according Python wrappers.'''
    print "Generating XML schema files ..."
    createFaultTreeSchema("FuzzEd/static/xsd/faulttree.xsd")
    createFuzzTreeSchema("FuzzEd/static/xsd/fuzztree.xsd")
    build_xmlschema_wrappers()

@task
def naturaldocs():
    '''Builds source code documentation in /docs.'''
    # Build natural docs in 'docs' subdirectory
    if not os.path.exists('docs'):
        os.mkdir('docs')
    if os.system('tools/NaturalDocs/NaturalDocs -i FuzzEd -xi FuzzEd/static/lib -o HTML docs -p docs ') != 0:
        raise Exception('Execution of NaturalDocs compiler failed.')

@task 
def configs(target='development'):
    '''Builds the configuration files for sub projects out of settings.ini'''
    assert(target in ['development','vagrant','production'])
    print 'Building configs...'
    f=open('FuzzEd/settings.py','w')
    f.write(createDjangoSettings('settings.ini', [target]))
    f.close()
    f=open('backends/daemon.ini','w')
    f.write(createBackendSettings('settings.ini', [target, 'backend_']))
    f.close()

def build_analysis_server_java():
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

@task
def css():
    '''Builds the CSS files for the project with lessc.'''
    os.system('lessc FuzzEd/static/less/theme/white/theme.less FuzzEd/static/css/theme/white.css')

@task()
def all():
    '''Builds all.'''
    css()
    shapes()
    xmlschemas()
    naturaldocs()
    notations()
    configs()
    backends()    

