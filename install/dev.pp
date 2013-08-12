import "common.pp"
import "java.pp"
import "prod_backend.pp"

# ANT is included in Mac OS X
if $operatingsystem != "Darwin" {
	package { "ant":
		ensure => latest;
	}
}

package { "django":
	ensure => "1.5",
	provider => pip;
}

package { [ "south", "openid2rp", "django-require" ]:
        ensure => latest,
        provider => "pip";
}

#TODO: Tweak settings.py for the correct configuration
