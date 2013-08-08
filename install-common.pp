$pip_latest = [ "south", "openid2rp", "django-require", "lxml", "pyxb", "psycopg2", "pyyaml", "beanstalkc" ]
package { $pip_latest: ensure => "latest", provider => "pip" }

package { "django":
	ensure => "1.5",
	provider => pip;
}


