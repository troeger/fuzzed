import "common.pp"
import "python.pp"
import "beanstalkd.pp"
import "latex.pp"

package { [ "pyxb", "beanstalkc" ]:
        ensure => latest,
        provider => "pip";
}

# JRE installation for compiling analysis server
if $operatingsystem == "Darwin" {
	# Java puppet module does not work on MacOS X so far
	notice("JRE 7 cannot be installed through Puppet on Mac OS X. Please do this manually.")
} else {
    class { 'java':
      distribution => 'jre',
      version      => 'latest',
    }
}

#TODO: Install init script for rendering service
