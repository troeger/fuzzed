$script = <<SCRIPT
if `tty -s`; then
   mesg n
fi

echo Provisioning Machine...
apt-get update
apt-get -y install build-essential make
apt-get -y install libreadline-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
apt-get -y install python python-dev python-pip
pip install fabric

echo Bootstrapping Dev Environment...
cd /home/fuzztrees
fab bootstrap_dev
fab build

SCRIPT

Vagrant::Config.run do |config|
    config.vm.box = "precise64"
    config.vm.box_url = "http://files.vagrantup.com/precise64.box"
    
    #config.vm.boot_mode = :gui
    
	config.vm.network :bridged
    config.vm.forward_port 8000, 8000

    config.vm.share_folder "fuzztrees", "/home/fuzztrees", "."

    config.vm.provision :shell, :inline => $script
end