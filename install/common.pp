package {"python": 
	ensure => "2.7",
	source => $operatingsystem ? {
    	"Darwin" => "http://python.org/ftp/python/2.7.5/python-2.7.5-macosx10.6.dmg",
	}
}

exec { "easy_install pip":
    path => "/usr/local/bin:/usr/bin:/bin",
    subscribe => Package['python'],
    unless => "which pip";
}

package { $pip_latest: 
	ensure => "latest", 
	provider => "pip"; 
}
