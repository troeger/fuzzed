# Puppet extension to support Oracle Java installation
if $operatingsystem == "Darwin" {
		notice("JDK 7 cannot be installed through Puppet on Mac OS X. Please do this manually.")
} else {
        module { 'puppetlabs/java':
          ensure     => present,
          modulepath => '/etc/puppet/modules',
        }
        class { 'java':
          distribution => 'jdk',
          version      => 'latest',
        }
}

