#./site_scons automatically becomes part of the Python search path
import builders

# Add our own stuff to the SCons environment
env = Environment()
builders.add_to_env(env)

# NaturalDocs generation - 'docs' target
natdocs = env.Command(	Dir('docs'), 
						Dir('FuzzEd'), 
						[
							Delete("docs"),
							Mkdir("docs"),
							'tools/NaturalDocs/NaturalDocs -i $SOURCE -o HTML $TARGET -p $TARGET'
						]
					 )
Clean(natdocs, 'docs')

# Lessc compilation - 'white.css' target
env.Lessc('FuzzEd/static/css/theme/white.css',
	      'FuzzEd/static/less/theme/white/theme.less')

# Config file generation - 'settings.py' and 'daemon.ini' target
env.DjangoConfig('FuzzEd/settings.py', 'settings.ini')
env.DaemonConfig('backends/daemon.ini', 'settings.ini')

# 'clean' target
env.Command('clean', [], 'scons -c')