import "common.pp"

module { 'puppetlabs/apache':
	  ensure     => present;
}

class { 'apache':
  default_vhost => false;
}

file { ["/var/www/fuzztrees.net", "/var/www/fuzztrees.net/www"]:
    ensure => "directory",
    owner  => "www-data",
    group  => "www-data",
    mode   => 750,
}

class { 'apache::mod::wsgi': }

apache::vhost { 'fuzztrees.net':
	servername => 'fuzztrees.net',
	port    => '80',
	docroot => '/var/www/fuzztrees.net/www/FuzzEd/',
	aliases => [ { alias => '/static', path => '/var/www/fuzztrees.net/www/FuzzEd/static-release' } ],
	directories => [
	    { path => '/usr/local/lib/python2.7/', options => ["FollowSymLinks"], override => "None", order => "deny,allow", allow => "from all" },
	],
	custom_fragment => " WSGIDaemonProcess fuzztrees.net processes=5 threads=1 maximum-requests=1000 display-name=%{GROUP} python-path=/var/www/fuzztrees.net/www/\nWSGIProcessGroup fuzztrees.net\nWSGIScriptAlias /  /var/www/fuzztrees.net/www/FuzzEd/wsgi.py"
}

apache::vhost { 'www.fuzztrees.net':
	servername => "www.fuzztrees.net",
	redirect_status => 'permanent',
	redirect_dest => 'http://fuzztrees.net',
	docroot => '/var/www/fuzztrees.net/www/FuzzEd/'
}

package { "postgresql":
	ensure => latest;
}

#TODO: Configure PostgreSQL database

package { "django":
	ensure => "1.5",
	provider => "pip";
}

# PIP package would need a PostgreSQL dev install
package { "python-psycopg2":
	ensure => latest;
}

package { [ "south", "openid2rp", "pyxb", "beanstalkc" ]:
        ensure => latest,
        provider => "pip";
}

#TODO: Tweak settings.py for the correct configuration
