'''
  The central SCons file for this project, which is based on a set of FuzzEd-specific
  builders stored in the site_scons folder.
'''

import os, platform, socket
from FuzzEd.settings import VERSION

#./site_scons automatically becomes part of the Python search path
# Add our own builders to the SCons environment
env=Environment(
  tools=['default', fuzzed_builders])  

# Decide which build mode we have here
# development: Prepare everything for Mac OS X machine in dev mode
# vagrant:     Prepare everything for Vagrant Ubuntu Trusty machine in dev mode
# production:  Prepare everything for Ubuntu Trusty machine in production
if socket.getfqdn() == 'vagrant-ubuntu-trusty-32':
    mode = "vagrant"
else:
    mode = "development"
assert(mode in ['development','vagrant','production'])
print "Building for "+mode+" mode"
env['mode']=mode

# Include SCons file for backend daemons
SConscript('backends/SConscript')

# Static files generation - 'static-release' target
statics = env.Command( Dir('FuzzEd/static-release'), 
                       Dir('FuzzEd/static'), 
                       './manage.py collectstatic -v3 --noinput'
                      )
Clean(statics, 'FuzzEd/static-release')

# Web package generation - 'package.web' target
package_web = env.Package(
                     "dist/FuzzEd-%s"%VERSION, 
                     [Dir("FuzzEd/api"),
                      Dir("FuzzEd/lib"),
                      Dir("FuzzEd/management"),
                      Dir("FuzzEd/migrations"),
                      Dir("FuzzEd/models"),
                      Dir("FuzzEd/static-release"),
                      Dir("FuzzEd/templates"),
                      Glob("FuzzEd/*"),
                     "manage.py"]
                  )
Alias('package.web', package_web)

# Backend package generation - 'package.backend' target
package_backend = env.Package(
                     "dist/FuzzEdBackend-%s"%VERSION, 
                     [Dir("backends/lib"),
                     "backends/initscript.sh",
                     "backends/daemon.py",
                     "backends/daemon.ini",
                     Dir("backends/rendering")]
                  )
Alias('package.backend', package_backend)

# NaturalDocs generation - 'docs' target
docs_targets = Dir('docs')
natdocs = env.Command(  docs_targets, 
                        Dir('FuzzEd'), 
                        [
                            Delete("docs"),
                            Mkdir("docs"),
                            'tools/NaturalDocs/NaturalDocs -i $SOURCE -o HTML $TARGET -p $TARGET'
                        ]
                     )
Clean(natdocs, 'docs')
Alias('docs', docs_targets)

# Lessc compilation - 'white.css' target
lessc_targets = 'FuzzEd/static/css/theme/white.css'
env.Lessc( lessc_targets,
          'FuzzEd/static/less/theme/white/theme.less')
Alias('css', lessc_targets)

# Config file generation - 'settings.py' and 'daemon.ini' target
config_targets = ['FuzzEd/settings.py', 'backends/daemon.ini']
env.FuzzedConfig( config_targets, 'settings.ini')
AlwaysBuild('settings')     # to support flipping betwenn Vagrant and native dev
Alias('settings', config_targets)

# XML Wrapper generation
xml_targets = [  'Fuzzed/models/xml_common.py',
               'Fuzzed/models/xml_configurations.py',
               'Fuzzed/models/xml_backend.py',
               'Fuzzed/models/xml_fuzztree.py',
               'Fuzzed/models/xml_faulttree.py'   ]
env.PyXB(   xml_targets,
            [  'FuzzEd/static/xsd/commonTypes.xsd',
               'FuzzEd/static/xsd/configurations.xsd',
               'FuzzEd/static/xsd/backendResult.xsd',
               'FuzzEd/static/xsd/fuzztree.xsd',
               'FuzzEd/static/xsd/faulttree.xsd' 
            ])
Alias('xml', xml_targets)

# Generation of Python version of the notation files 
notation_targets = 'FuzzEd/models/notations.py'
env.Notations(  notation_targets,
              [ 'FuzzEd/static/notations/dfd.json',
                'FuzzEd/static/notations/faulttree.json',
                'FuzzEd/static/notations/fuzztree.json',
                'FuzzEd/static/notations/rbd.json'] )
Alias('notations', notation_targets)

# Generation of the TikZ library code, based on SVG images
tikz_targets = 'FuzzEd/models/node_rendering.py'
env.Tikz( tikz_targets, 
          Glob('FuzzEd/static/img/dfd/*.svg') +
          Glob('FuzzEd/static/img/faulttree/*.svg') +
          Glob('FuzzEd/static/img/fuzztree/*.svg') +
          Glob('FuzzEd/static/img/rbd/*.svg') )
Alias('shapes', tikz_targets)

# Generate patched versions of third patry code
env.Patch('FuzzEd/static/css/font-awesome/font-awesome-4.1.0.css',
          ['FuzzEd/static/css/font-awesome/font-awesome-4.1.0.css.patch',
           'FuzzEd/static/css/font-awesome/font-awesome-4.1.0.css.orig'])
env.Patch('FuzzEd/static/css/font-awesome/font-awesome-4.1.0.min.css',
          ['FuzzEd/static/css/font-awesome/font-awesome-4.1.0.min.css.patch',
           'FuzzEd/static/css/font-awesome/font-awesome-4.1.0.min.css.orig'])
env.Patch('FuzzEd/static/lib/jquery-ui/jquery-ui-1.10.3.js',
          ['FuzzEd/static/lib/jquery-ui/jquery-ui-1.10.3.js.patch',
           'FuzzEd/static/lib/jquery-ui/jquery-ui-1.10.3.js.orig'])


# Default targets when nothing is specified
#env.Default('docs', 'css', 'settings', 'xml', 'notations', 'shapes',
#            'ftanalysis', 'ftsimulation')

# Special pseudo-targets to run stuff via Scons
AlwaysBuild(env.Command('run.server', None, server))
AlwaysBuild(env.Command('run.backend', None, backend))
AlwaysBuild(env.Command('run.tests', None, tests))
AlwaysBuild(env.Command('fixture.save', None, fixture_save))


