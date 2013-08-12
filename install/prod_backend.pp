#TODO: Test this on Linux

import "common.pp"
import "java.pp"

package { "beanstalkd":
	ensure => latest;
}

package { "texlive":
	ensure => latest;
}

package { [ "pyxb", "beanstalkc" ]:
        ensure => latest,
        provider => "pip";
}

#TODO: Install init script for rendering service
