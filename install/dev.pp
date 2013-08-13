# Puppet manifest for installing a developer machine
# It includes both the web frontend and all the backend software

import "common.pp"

#####################
# class definitions #
#####################

class build_preparation {
	exec { "build_schema_wrappers":
	    command => "/usr/bin/env python setup.py build";
	} ->
	exec { "create_db":
	    command => "/usr/bin/env python manage.py syncdb";
	}
}

############################################
# class declaration with relevant ordering #
############################################

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
