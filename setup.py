#!/usr/bin/env python

# Using distribute enhancements for setuptools
import distribute_setup
distribute_setup.use_setuptools()
from setuptools import setup
from distutils.command.build import build as _build
from distutils.command.clean import clean as _clean

import os

# check FuzzEd/__init__.py for the project version number
from FuzzEd import __version__

def build_naturaldocs():
	# Build natural docs in 'docs' subdirectory
	if not os.path.exists("docs"):
		os.mkdir("docs")
	os.system("tools/NaturalDocs/NaturalDocs -i FuzzEd -o HTML docs -p docs")

def build_django_require():
	# Use Django collectstatic, which triggers django-require optimization
	os.system("./manage.py collectstatic -v3 --noinput")

def clean_pycs():
	# Clean all pyc files recursively
	for root, dirs, files in os.walk('FuzzEd'):
		for name in files:
			if name.endswith(".pyc"):
				fullname = os.path.join(root, name) 
				print("Removing "+fullname)
				os.remove(fullname)

# Our overloaded 'setup.py build' command
class build(_build):
	def run(self):
		_build.run(self)
		build_naturaldocs()
		build_django_require()

# Our overloaded 'setup.py clean' command
class clean(_clean):
	def run(self):
		_clean.run(self)
		os.system("rm -rf docs")
		clean_pycs()

setup(
	name = 'FuzzEd',
	version = __version__,
	install_requires=[
		'django',
		'south',
		'openid2rp',
		'django-require'
	],
	packages = ['FuzzEd'],
	include_package_data = True,
	cmdclass={'build': build, 'clean': clean},
	maintainer = "Peter Troeger",
	maintainer_email ="peter.troeger@hpi.uni-potsdam.de",
	url = "https://bitbucket.org/troeger/fuzztrees"
)
