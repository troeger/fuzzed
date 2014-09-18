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

VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = "ubuntu/trusty32"
    config.vm.network "private_network", ip: "192.168.33.10"
    config.vm.synced_folder ".", "/home/vagrant/fuzzed"

    config.vm.provider "virtualbox" do |v|
      # Taken from http://www.stefanwrobel.com/how-to-make-vagrant-performance-not-suck
      host = RbConfig::CONFIG['host_os']
      if host =~ /darwin/
        cpus = `sysctl -n hw.ncpu`.to_i
        # sysctl returns Bytes and we need to convert to MB
        mem = `sysctl -n hw.memsize`.to_i / 1024 / 1024 / 2
      elsif host =~ /linux/
        cpus = `nproc`.to_i
        # meminfo shows KB and we need to convert to MB
        mem = `grep 'MemTotal' /proc/meminfo | sed -e 's/MemTotal://' -e 's/ kB//'`.to_i / 1024 / 2
      else # sorry Windows folks, I can't help you
        cpus = 2
        mem = 1024
      end
      v.customize ["modifyvm", :id, "--memory", mem]
      v.customize ["modifyvm", :id, "--cpus", cpus]
    end

    config.vm.provision "shell", inline: $provisioning_script
end
