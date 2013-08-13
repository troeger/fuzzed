# Puppet manifest for installing a compute backend machine

import "common.pp"

class { 'puppet_config':
	stage => pre1,
}

class { 'python27_and_pip':
	stage => pre2,
}

package { [ "pyxb", "beanstalkc" ]:
        ensure => latest,
        provider => "pip";
}

include beanstalkd
include latex
include jre

#TODO: Install init script for rendering service
