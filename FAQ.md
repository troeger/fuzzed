# Frequently Asked Questions

## Vagrant has problems mounting the shared folders.

Upgrade to the very last VirtualBox >= 4.3.12. Make sure that you use the Uninstall script beforehand, and re-create all VM's to get the latest guest additions:

https://www.virtualbox.org/wiki/Download_Old_Builds_4_3
http://download.virtualbox.org/virtualbox/4.3.8/
https://github.com/mitchellh/vagrant/issues/3341

## Vagrant box has no internet connectivity.

In the Vagrantfile, uncomment the following lines, then re-provision:

config.vm.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
config.vm.customize ["modifyvm", :id, "--natdnsproxy1", "on"]