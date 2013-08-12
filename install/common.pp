# Install Puppet extension to support Homebrew on Darwin
# Furthermore, Homebrew has no python2.7 package, but installs it by default
if $operatingsystem == "Darwin" {
	module { 'bjoernalbers/homebrew':
	  ensure     => present,
	  modulepath => '/etc/puppet/modules',
	}
	include homebrew
	Package { provider => "brew" }
	package {"python": 
		ensure => latest;
	}
}
else {
	package {"python2.7": 
		ensure => latest;
	}
}

# Homebrew brings PIP automatically together with the Python 2.7 brew
if $operatingsystem != "Darwin" {
	package {"python-pip":
		ensure => latest;
	}
}

