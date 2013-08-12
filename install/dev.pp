$pip_latest = [ "south", "openid2rp", "django-require", "pyxb", "beanstalkc" ]

import "common.pp"

package { "java":
	ensure => "7",
	provider => "brew";
}

package { "ant":
	ensure => latest,
	subscribe => "java";
}

package { "beanstalkd":
	ensure => "latest";
}

package { "django":
	ensure => "1.5",
	provider => pip;
}
