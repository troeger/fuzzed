$pip_latest = [ "south", "openid2rp", "django-require", "pyxb", "beanstalkc" ]

include common.pp

class { "java":
	version => "7",
	distribution => "jdk";
}

package { "ant":
	version => latest,
	subscribe => "java";
}

package { "beanstalkd":
	ensure => "latest";
}

package { "django":
	ensure => "1.5",
	provider => pip;
}
