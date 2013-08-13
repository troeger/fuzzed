# Puppet manifest for installing a developer machine
# It includes both the web frontend and all the backend software

import "common.pp"

# class definitions

class build_preparation {
	exec { "build_schema_wrappers":
	    command => "/usr/bin/env python setup.py build";
	} ->
	exec { "create_db":
	    command => "/usr/bin/env python manage.py syncdb";
	}
}

class jdk {
	# JDK installation for compiling analysis server
	if $operatingsystem == "Darwin" {
		# Java puppet module does not work on MacOS X so far
		err("JDK 7 cannot be installed through Puppet on Mac OS X. Please do this manually.")
		# ANT is included in Mac OS X
	} else {
	    class { 'java':
	      distribution => 'jdk',
	      version      => 'latest';
	    }
		package { "ant":
			ensure => latest;
		}
	}
}

# class declarations with relevant ordering

class { 'puppet_config':
	stage => pre1,
}

class { 'python27_and_pip':
	stage => pre2,
}

include django
include latex
include beanstalkd
include jdk
package { [ "south", "openid2rp", "django-require", "pyxb", "beanstalkc" ]:
        ensure => latest,
        provider => "pip";
}

class { 'build_preparation':
	stage => last,
}

#TODO: Tweak settings.py for the correct configuration
