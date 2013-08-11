$pip_latest = [ "south", "openid2rp", "pyxb", "psycopg2", "beanstalkc" ]

include common.pp

package { "postgresql":
	version => latest;
}

package { "django":
	ensure => "1.5",
	provider => pip;
}

