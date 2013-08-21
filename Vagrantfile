$script = <<SCRIPT
echo Provisioning Machine...

apt-get install build-essential make
apt-get install libreadline-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

cd ~/Downloads/
wget http://python.org/ftp/python/2.7.5/Python-2.7.5.tgz
tar -xvf Python-2.7.5.tgz
cd Python-2.7.5
./configure
make
make install

apt-get install python-setuptools
easy_install pip
pip install virtualenv

SCRIPT

Vagrant::Config.run do |config|
    config.vm.box = "precise64"
    config.vm.box_url = "http://files.vagrantup.com/precise64.box"
    config.vm.boot_mode = :gui

    #config.vm.forward_port 80, 8080 
    #config.vm.forward_port 8000, 8001

    config.vm.provision :shell, :inline => $script
end