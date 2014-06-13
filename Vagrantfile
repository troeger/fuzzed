$provisioning_script = <<SCRIPT
  apt-get update
  apt-get install -y python-dev python-pip
  sudo pip install ansible
  cd fuzztrees
  sudo ansible-playbook -i ansible/dev_machine ansible/site.yml 
SCRIPT

Vagrant::Config.run do |config|
    config.vm.box = "ubuntu/trusty32"
    config.vm.network :hostonly, "192.168.33.10"
    config.vm.share_folder  "fuzztrees", "/home/vagrant/fuzztrees", "."
    # If the VM has no internet connectivity, uncomment this line:
    # config.vm.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    # config.vm.customize ["modifyvm", :id, "--natdnsproxy1", "on"]

#   This is how the ansible provider normally would be used. Since Ansible
#   is not supported on Windows, we need the alternative strategy of running
#   something shell magic inside of the VM

#   config.vm.provision "ansible" do |ansible|
#       ansible.playbook = "ansible/site.yml"
#       ansible.extra_vars = { ansible_ssh_user: 'vagrant' }
#       ansible.sudo = true
#       ansible.verbose = "vvvv"
#       ansible.groups = {
#                          "devmachine" => ["default"]
#       }        
#   end
    config.vm.provision "shell", inline: $provisioning_script
end
