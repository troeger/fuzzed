$pip_latest = [ "south", "openid2rp", "django-require", "pyxb", "beanstalkc" ]

import "common.pp"
import "java.pp"

# ANT is included in Mac OS X
if $operatingsystem != "Darwin" {
	package { "ant":
		ensure => latest;
	}
}

package { "beanstalkd":
	ensure => latest;
}

package { "django":
	ensure => "1.5",
	provider => pip;
}

package { $::pip_latest:
        ensure => latest,
        provider => "pip";
}

#TODO: Tweak settings.py for the correct configuration
