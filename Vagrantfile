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
echo ...done.

echo Bootstrapping Dev Environment...
cd /home/fuzztrees
fab bootstrap_dev
echo ...done.

echo Building Dev Environment...
fab build
echo ...done.

SCRIPT

Vagrant::Config.run do |config|
    config.vm.box = "precise64"
    config.vm.box_url = "https://dl.dropboxusercontent.com/u/165709740/boxes/precise64-vanilla.box"
    
    #"https://dl.dropboxusercontent.com/u/547671/thinkstack-raring64.box"
    config.vm.boot_mode = :gui
	#config.vm.network :bridged
    config.vm.forward_port 8000, 8080
    config.vm.network :hostonly, "192.168.33.10"
    #config.vm.network :hostonly, "33.33.33.10"

    config.vm.share_folder "fuzztrees", "/home/fuzztrees", "."

    config.vm.provision :shell, :inline => $script
end