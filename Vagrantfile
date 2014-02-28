$script = <<SCRIPT
echo Provisioning Machine...
sudo apt-get update
sudo apt-get -y install python-software-properties
sudo add-apt-repository -y ppa:george-edison55/gcc4.7-precise
sudo add-apt-repository -y ppa:chris-lea/node.js
sudo apt-get update
sudo apt-get -y install build-essential make gcc-4.7 g++-4.7
sudo apt-get -y install python python-dev python-pip perl
sudo pip install fabric
echo ...done.
echo Bootstrapping Dev Environment...
echo "cd /home/fuzztrees" >> /home/vagrant/.bashrc
cd /home/fuzztrees
fab bootstrap.dev
echo ...done.
echo Building Dev Environment with Vagrant support...
fab build.all
echo ...done.
SCRIPT

Vagrant::Config.run do |config|
    config.vm.box = "precise64"
    config.vm.box_url = "http://files.vagrantup.com/precise64.box"

    config.vm.network :hostonly, "192.168.33.10"
   
    config.vm.share_folder "fuzztrees", "/home/fuzztrees", "."

    config.vm.provision :shell, :inline => $script
end
