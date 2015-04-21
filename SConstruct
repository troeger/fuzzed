'''
  The central SCons file for this project, which is based on a set of FuzzEd-specific
  builders stored in the site_scons folder.
'''

import os, platform, socket

if "DJANGO_CONFIGURATION" not in os.environ:
  # Not set by user, so we assume developer mode, since
  # production systems are supposed to not use this script
  os.environ["DJANGO_CONFIGURATION"]="Dev"
  print("Assuming Dev mode")

from FuzzEd import VERSION

#./site_scons automatically becomes part of the Python search path
# Add our own builders to the SCons environment
env=Environment(
  tools=['default', fuzzed_builders])  

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

# Backend package generation - 'package.backend' target
package_backend = env.Package(
                     "dist/FuzzEdBackend-%s"%VERSION, 
                     [Dir("backends/lib"),
                     "backends/initscript.sh",
                     "backends/daemon.py",
                     "backends/daemon.ini",
                     Dir("backends/rendering")]
                  )

gittag = AlwaysBuild(env.Command('git tag %s'%VERSION, None, 'git tag v%s'%VERSION))

Alias('package', gittag)
Alias('package', package_web)
Alias('package', package_backend)

# Lessc compilation - 'white.css' target
css = env.Lessc( 'FuzzEd/static/css/theme/white.css',
          'FuzzEd/static/less/theme/white/theme.less')

# XML Wrapper generation
xml_targets = [  'Fuzzed/models/xml_common.py',
               'Fuzzed/models/xml_configurations.py',
               'Fuzzed/models/xml_backend.py',
               'Fuzzed/models/xml_fuzztree.py',
               'Fuzzed/models/xml_faulttree.py'   ]
xml = env.PyXB(   xml_targets,
            [  'FuzzEd/static/xsd/commonTypes.xsd',
               'FuzzEd/static/xsd/configurations.xsd',
               'FuzzEd/static/xsd/backendResult.xsd',
               'FuzzEd/static/xsd/fuzztree.xsd',
               'FuzzEd/static/xsd/faulttree.xsd' 
            ])

# Generation of Python version of the notation files 
notations = env.Notations(  'FuzzEd/models/notations.py',
              [ 'FuzzEd/static/notations/dfd.json',
                'FuzzEd/static/notations/faulttree.json',
                'FuzzEd/static/notations/fuzztree.json',
                'FuzzEd/static/notations/rbd.json'] )

# Generation of the TikZ library code, based on SVG images
shapes = env.Tikz( 'FuzzEd/models/node_rendering.py', 
          Glob('FuzzEd/static/img/dfd/*.svg') +
          Glob('FuzzEd/static/img/faulttree/*.svg') +
          Glob('FuzzEd/static/img/fuzztree/*.svg') +
          Glob('FuzzEd/static/img/rbd/*.svg') )

# Generate patched versions of third party code
patch1 = env.Patch('FuzzEd/static/css/font-awesome/font-awesome-4.1.0.css',
          ['FuzzEd/static/css/font-awesome/font-awesome-4.1.0.css.patch',
           'FuzzEd/static/css/font-awesome/font-awesome-4.1.0.css.orig'])
patch2 = env.Patch('FuzzEd/static/css/font-awesome/font-awesome-4.1.0.min.css',
          ['FuzzEd/static/css/font-awesome/font-awesome-4.1.0.min.css.patch',
           'FuzzEd/static/css/font-awesome/font-awesome-4.1.0.min.css.orig'])
patch3 = env.Patch('FuzzEd/static/lib/jquery-ui/jquery-ui-1.10.3.js',
          ['FuzzEd/static/lib/jquery-ui/jquery-ui-1.10.3.js.patch',
           'FuzzEd/static/lib/jquery-ui/jquery-ui-1.10.3.js.orig'])
patch4 = env.Patch('FuzzEd/static/lib/jquery-ui/jquery-ui-1.10.3.min.js',
          ['FuzzEd/static/lib/jquery-ui/jquery-ui-1.10.3.min.js.patch',
           'FuzzEd/static/lib/jquery-ui/jquery-ui-1.10.3.min.js.orig'])

# Define meta-targets for ease of use
env.Alias("backend", "ftconfiguration")
env.Alias("backend", "ftanalysis")
env.Alias("backend", "ftsimulation")

env.Alias("frontend", css)
env.Alias("frontend", xml)
env.Alias("frontend", notations)
env.Alias("frontend", shapes)
env.Alias("frontend", patch1)
env.Alias("frontend", patch2)
env.Alias("frontend", patch3)
env.Alias("frontend", patch4)

# Default targets when nothing is specified
# We skip the backend and doc builds here, which mainly is speeding
# up frontend development
env.Default("frontend")

# Special pseudo-targets to run stuff via Scons
AlwaysBuild(env.Command('fixture.save', None, fixture_save))
AlwaysBuild(env.Command('run.server', None, server))
AlwaysBuild(env.Command('run.backend', None, backend))


