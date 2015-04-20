VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = "ubuntu/trusty32"
    config.vm.network "private_network", ip: "192.168.33.10"
    config.vm.hostname = "vagrant.fuzzed.org"    # Crucial for OAuth2 callbacks to work, we donate the DNS entry for that
    config.vm.synced_folder ".", "/home/vagrant/fuzzed", type: "nfs"

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

    config.vm.provision "ansible" do |ansible|
      ansible.playbook = "ansible/site.yml"
      ansible.groups = { "devmachine" => ["default"] }
      ansible.extra_vars = { ansible_ssh_user: "vagrant", 
                             vagrant: true,
                             virtualenvpath: "~/fuzzed_venv/" }
    end
end
