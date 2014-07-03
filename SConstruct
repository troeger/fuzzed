'''
  The central SCons file for this project, which is based on a set of FuzzEd-specific
  builders stored in the site_scons folder.

  TODO:
    - Add clean target for .pyc files.
'''

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
#VariantDir('Fuzzed/models','FuzzEd/static/xsd')
env.PyXB(   [  'Fuzzed/models/xml_common.py',
               'Fuzzed/models/xml_configurations.py',
               'Fuzzed/models/xml_backend.py',
               'Fuzzed/models/xml_fuzztree.py',
               'Fuzzed/models/xml_faulttree.py'   ],
            [  'FuzzEd/static/xsd/commonTypes.xsd',
               'FuzzEd/static/xsd/configurations.xsd',
               'FuzzEd/static/xsd/backendResult.xsd',
               'FuzzEd/static/xsd/fuzztree.xsd',
               'FuzzEd/static/xsd/faulttree.xsd' 
            ])

env.Notations(  'FuzzEd/models/notations.py',
              [ 'FuzzEd/static/notations/dfd.json',
                'FuzzEd/static/notations/faulttree.json',
                'FuzzEd/static/notations/fuzztree.json',
                'FuzzEd/static/notations/rbd.json'] )

env.Tikz( 'FuzzEd/models/node_rendering.py', 
          Glob('FuzzEd/static/img/dfd/*.svg') +
          Glob('FuzzEd/static/img/faulttree/*.svg') +
          Glob('FuzzEd/static/img/fuzztree/*.svg') +
          Glob('FuzzEd/static/img/rbd/*.svg') )


