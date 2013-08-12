# Puppet extension to support Homebrew on Darwin
if $operatingsystem == "Darwin" {
	module { 'bjoernalbers/homebrew':
	  ensure     => present,
	  modulepath => '/etc/puppet/modules',
	}
	include homebrew
	Package { provider => "brew" }
}

package {"python2.7": 
	ensure => latest;
}

# Homebrew brings PIP automatically together with the Python 2.7 brew
if $operatingsystem != "Darwin" {
	package {"python-pip":
		ensure => latest;
	}
}

