class { "java":
	version => "7",
	distribution => "jre";
}

package { "beanstalkd":
	ensure => "latest";
}

packacke { "latex":
	ensure => "latest";
}
