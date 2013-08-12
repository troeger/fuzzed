# Puppet extension to support Oracle Java installation
if $operatingsystem != "Darwin" {
        #TODO: This module does not support Darwin, print notice about manual installation
        module { 'puppetlabs/java':
          ensure     => present,
          modulepath => '/etc/puppet/modules',
        }
        class { 'java':
          distribution => 'jdk',
          version      => 'latest',
        }
}

