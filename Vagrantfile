$script = <<SCRIPT
echo Provisioning Machine...

apt-get -y install build-essential make
apt-get -y install libreadline-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
apt-get -y install python python-setuptools python-pip

SCRIPT

Vagrant::Config.run do |config|
    config.vm.box = "precise64"
    config.vm.box_url = "http://files.vagrantup.com/precise64.box"
    #config.vm.boot_mode = :gui

    #config.vm.forward_port 80, 8080 
    #config.vm.forward_port 8000, 8001

    config.vm.provision :shell, :inline => $script
end