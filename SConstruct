'''
  The central SCons file for this project, which is based on a set of FuzzEd-specific
  builders stored in the site_scons folder.
'''

VERSION="0.7.6"

#./site_scons automatically becomes part of the Python search path
# Add our own builders to the SCons environment
env=Environment(
  tools=['default', fuzzed_builders])  

# Include SCons file for backend daemons
SConscript('back/SConscript')

# Static files generation - 'static-release' target
statics = env.Command( Dir('front/FuzzEd/static-release'), 
                       Dir('front/FuzzEd/static'), 
                       './manage.py collectstatic -v3 --noinput --configuration=Dev'
                      )
Clean(statics, 'front/FuzzEd/static-release')

# Lessc compilation - 'white.css' target
css = env.Command( Dir('front/FuzzEd/static/css/theme'),
                   Dir('front/FuzzEd/static/less/theme/white'),
                   'lesscpy theme.less -o front/FuzzEd/static/css/theme')

# XML Wrapper generation
xml_targets = ['front/FuzzEd/models/xml_common.py',
               'front/FuzzEd/models/xml_configurations.py',
               'front/FuzzEd/models/xml_backend.py',
               'front/FuzzEd/models/xml_fuzztree.py',
               'front/FuzzEd/models/xml_faulttree.py'   ]
xml = env.PyXB(   xml_targets,
            [  'front/FuzzEd/static/xsd/commonTypes.xsd',
               'front/FuzzEd/static/xsd/configurations.xsd',
               'front/FuzzEd/static/xsd/backendResult.xsd',
               'front/FuzzEd/static/xsd/fuzztree.xsd',
               'front/FuzzEd/static/xsd/faulttree.xsd' 
            ])

# Web package generation - 'package.web' target
package_web = env.Package(
                     "dist/FuzzEd-%s"%VERSION, 
                     [Dir("front/FuzzEd/api"),
                      Dir("front/FuzzEd/management"),
                      Dir("front/FuzzEd/migrations"),
                      Dir("front/FuzzEd/models"),
                      Dir("front/FuzzEd/static-release"),
                      Dir("front/FuzzEd/templates"),
                      xml_targets,
                      Glob("FuzzEd/*"),
                     "manage.py"]
                  )

# Backend package generation - 'package.backend' target
package_backend = env.Package(
                     "dist/FuzzEdBackend-%s"%VERSION, 
                     [Dir("back/lib"),
                     "back/initscript.sh",
                     "back/daemon.py",
                     "back/daemon.ini",
                     Dir("back/rendering")]
                  )

gittag = AlwaysBuild(env.Command('git tag -f %s'%VERSION, None, 'git tag -f v%s'%VERSION))

Alias('package', gittag)
Alias('package', package_web)
Alias('package', package_backend)
Alias('package.web', package_web)


# Generation of Python version of the notation files 
notations = env.Notations(  'front/FuzzEd/models/notations.py',
              [ 'front/FuzzEd/static/notations/dfd.json',
                'front/FuzzEd/static/notations/faulttree.json',
                'front/FuzzEd/static/notations/fuzztree.json',
                'front/FuzzEd/static/notations/rbd.json'] )

# Generation of the TikZ library code, based on SVG images
shapes = env.Tikz( 'front/FuzzEd/models/node_rendering.py', 
          Glob('front/FuzzEd/static/img/dfd/*.svg') +
          Glob('front/FuzzEd/static/img/faulttree/*.svg') +
          Glob('front/FuzzEd/static/img/fuzztree/*.svg') +
          Glob('front/FuzzEd/static/img/rbd/*.svg') )

# Generate patched versions of third party code
patch1 = env.Patch('front/FuzzEd/static/css/font-awesome/font-awesome-4.1.0.css',
          ['front/FuzzEd/static/css/font-awesome/font-awesome-4.1.0.css.patch',
           'front/FuzzEd/static/css/font-awesome/font-awesome-4.1.0.css.orig'])
patch2 = env.Patch('front/FuzzEd/static/css/font-awesome/font-awesome-4.1.0.min.css',
          ['front/FuzzEd/static/css/font-awesome/font-awesome-4.1.0.min.css.patch',
           'front/FuzzEd/static/css/font-awesome/font-awesome-4.1.0.min.css.orig'])
patch3 = env.Patch('front/FuzzEd/static/lib/jquery-ui/jquery-ui-1.10.3.js',
          ['front/FuzzEd/static/lib/jquery-ui/jquery-ui-1.10.3.js.patch',
           'front/FuzzEd/static/lib/jquery-ui/jquery-ui-1.10.3.js.orig'])
patch4 = env.Patch('front/FuzzEd/static/lib/jquery-ui/jquery-ui-1.10.3.min.js',
          ['front/FuzzEd/static/lib/jquery-ui/jquery-ui-1.10.3.min.js.patch',
           'front/FuzzEd/static/lib/jquery-ui/jquery-ui-1.10.3.min.js.orig'])

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
AlwaysBuild(env.Command('run.frontend', None, run_frontend))
AlwaysBuild(env.Command('run.backend', None, run_backend))
AlwaysBuild(env.Command('run.all', None, run_all))


