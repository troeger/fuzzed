$pip_latest = [ "south", "openid2rp", "django-require", "pyxb", "beanstalkc" ]

import "common.pp"

# ANT is included in Mac OS X
if $operatingsystem != "Darwin" {
	package { "ant":
		ensure => latest;
	}
}

package { "beanstalkd":
	ensure => "latest",
	provider => $operatingsystem ? {
    	"Darwin" => brew,
	}	
}

package { "django":
	ensure => "1.5",
	provider => pip;
}
