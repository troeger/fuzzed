$provisioning_script = <<SCRIPT
  export LANGUAGE=en_US.UTF-8
  export LANG=en_US.UTF-8
  export LC_ALL=en_US.UTF-8
  locale-gen en_US.UTF-8
  dpkg-reconfigure locales
  apt-get update
  apt-get install -y python-dev python-pip
  sudo pip install ansible
  cd fuzzed
  cp ansible/vagrant_machine /tmp/vagrant_machine
  sudo chmod -x /tmp/vagrant_machine
  sudo ansible-playbook -i /tmp/vagrant_machine ansible/site.yml 
SCRIPT

Vagrant::Config.run do |config|
    config.vm.box = "ubuntu/trusty32"
    config.vm.network :hostonly, "192.168.33.10"
    config.vm.share_folder  "fuzztrees", "/home/vagrant/fuzzed", "."
    # If the VM has no internet connectivity, uncomment this line:
    # config.vm.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    # config.vm.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
    config.vm.provision "shell", inline: $provisioning_script
end
