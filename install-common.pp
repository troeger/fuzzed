package {"python": 
	ensure => installed,
	source => $operatingsystem ? {
    	"Darwin" => "http://python.org/ftp/python/2.7.5/python-2.7.5-macosx10.6.dmg",
	}
}

exec { "easy_install pip":
    path => "/usr/local/bin:/usr/bin:/bin",
    unless => "which pip";
}

$pip_latest = [ "south", "openid2rp", "django-require", "lxml", "pyxb", "psycopg2", "pyyaml", "beanstalkc" ]

package { $pip_latest: 
	ensure => "latest", 
	provider => "pip"; 
}

package { "django":
	ensure => "1.5",
	provider => pip;
}



