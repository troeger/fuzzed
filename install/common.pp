# Puppet extension to support Oracle Java installation
if $operatingsystem != "Darwin" {
	#TODO: This module does not support Darwin, print notice about manual installation
	module { 'puppetlabs/java':
	  ensure     => present,
	  modulepath => '/etc/puppet/modules',
	}
}

# Puppet extension to support Homebrew on Darwin
#TODO: Do this only on Darwin
module { 'bjoernalbers/homebrew':
  ensure     => present,
  modulepath => '/etc/puppet/modules',
}
include homebrew

#TODO: Homebrew brings pip automatically; For Linux, we need to install it separately to Python
package {"python": 
	provider => $operatingsystem ? {
    	"Darwin" => brew,
	}	
}

# Install all the packages demanded from PIP
package { $pip_latest: 
	ensure => "latest", 
	provider => "pip"; 
}
