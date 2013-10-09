$script = <<SCRIPT
if `tty -s`; then
   mesg n
fi

echo Provisioning Machine...
apt-get -y install python-software-properties
add-apt-repository ppa:george-edison55/gcc4.7-precise
apt-get update
apt-get -y install build-essential make gcc-4.7 g++-4.7
apt-get -y install python python-dev python-pip perl
pip install fabric
echo ...done.

echo Bootstrapping Dev Environment...
cd /home/fuzztrees
fab bootstrap.dev
echo ...done.

echo Building Dev Environment...
fab build.all
echo ...done.

SCRIPT

Vagrant::Config.run do |config|
    config.vm.box = "precise64"
    config.vm.box_url = "https://dl.dropboxusercontent.com/u/165709740/boxes/precise64-vanilla.box"

    config.vm.forward_port 8000, 8080
    config.vm.network :hostonly, "192.168.33.10"
   
    config.vm.share_folder "fuzztrees", "/home/fuzztrees", "."

    config.vm.provision :shell, :inline => $script
end