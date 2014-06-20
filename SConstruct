import os

#./site_scons automatically becomes part of the Python search path
# Add our own builders to the SCons environment
env=Environment(tools=['default', fuzzed_builders])

# NaturalDocs generation - 'docs' target
natdocs = env.Command(  Dir('docs'), 
                        Dir('FuzzEd'), 
                        [
                            Delete("docs"),
                            Mkdir("docs"),
                            'tools/NaturalDocs/NaturalDocs -i $SOURCE -o HTML $TARGET -p $TARGET'
                        ]
                     )
# Remove 'docs' (dir) target on clean call
Clean(natdocs, 'docs')

# Lessc compilation - 'white.css' target
env.Lessc('FuzzEd/static/css/theme/white.css',
          'FuzzEd/static/less/theme/white/theme.less')

# Config file generation - 'settings.py' and 'daemon.ini' target
env.FuzzedConfig(['FuzzEd/settings.py', 'backends/daemon.ini'], 'settings.ini')

# XML Wrapper generation
env.PyXB('Fuzzed/models/xml_backend.py','FuzzEd/static/xsd/backendResult.xsd')
env.PyXB('Fuzzed/models/xml_fuzztree.py','FuzzEd/static/xsd/fuzztree.xsd')
env.PyXB('Fuzzed/models/xml_faulttree.py','FuzzEd/static/xsd/faulttree.xsd')
env.PyXB('Fuzzed/models/xml_common.py','FuzzEd/static/xsd/commonTypes.xsd')
env.PyXB('Fuzzed/models/xml_configurations.py','FuzzEd/static/xsd/configurations.xsd')

# Generate SVG name collection recursively
def get_svg_names(startdir='FuzzEd/static/img', covered=[]):
    for root, dirs, files in os.walk(startdir):
        for d in dirs:
            covered += get_svg_names(root+d,covered)
        for f in files:
            fullname = root+os.sep+f
            if fullname.endswith('.svg') and fullname not in covered:
                covered.append(fullname)
    return covered

env.Tikz('FuzzEd/models/node_rendering.py', get_svg_names())

