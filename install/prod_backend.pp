#TODO: Test this on Linux

import "common.pp"
import "java.pp"

package { "beanstalkd":
	ensure => latest;
}

if $operatingsystem == "Darwin" {
	notice("Latex cannot be installed through Puppet on Mac OS X. Please do this manually.")
} else {
	package { "texlive":
		ensure => latest;
	}
}

package { [ "pyxb", "beanstalkc" ]:
        ensure => latest,
        provider => "pip";
}

#TODO: Install init script for rendering service
