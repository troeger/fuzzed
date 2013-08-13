# Some preparations for the puppet operation

# Define custom stages
stage { 'pre2': 
     before => Stage['main'],
}
stage { 'pre1': 
     before => Stage['pre2'],
}
stage { 'last': }
Stage['main'] -> Stage['last']

# Enable homebrew usage on Darwin
if $operatingsystem == "Darwin" {
	# Install Puppet extension to support Homebrew on Darwin
	module { 'bjoernalbers/homebrew':
	  ensure     => present,
	  modulepath => '/etc/puppet/modules',
	}
	include homebrew
	Package { provider => "brew" }
	notice("Using homebrew for software installation.")
}

# Our custom classes used in different constellations

class puppet_config {
	module { 'puppetlabs/java':
	  ensure     => present;
	}

	module { 'puppetlabs/apache':
		  ensure     => present;
	}
}

class python27_and_pip {
	# Homebrew has no python2.7 package, but installs it by default
	if $operatingsystem == "Darwin" {
		package {"python": 
			ensure => latest;
		}
	}
	else {
		package {"python2.7": 
			ensure => latest;
		}
		package {"python-pip":
			ensure => latest;
		}
	}
}

class django {
	package { "django":
		ensure => "1.5",
		provider => pip;
	}	
}

class latex {
	if $operatingsystem == "Darwin" {
		err("Latex cannot be installed through Puppet on Mac OS X. Please do this manually.")
	} else {
		package { "texlive":
			ensure => latest;
		}
	}
}

class beanstalkd {
	package { "beanstalkd":
		ensure => latest;
	}
}
