# FuzzEd

## Preparation of development machine

The recommend development mode is with Vagrant. The Vagrantfile installs all relevant stuff in the virtual machine. Inside the Vagrant VM, you can find all sources at /home/fuzztrees. Just install Vagrant and run:

`vagrant up`

If you prefer to develop on your native machine without any virtualization, it needs Python, PIP and Ansible  (version 1.6 or higher is required). Then run:

`ansible-playbook -i ansible/dev_machine ansible/site.yml`

Add a "-s" option if you want to avoid working as root by using 'sudo'.

The Ansible code is prepared for Linux and Mac OS X development machines.

## Developing for FuzzEd

#### Compile static stuff                              

`> scons`

#### Synchronize local database with current model

`> ./manage.py migrate`

#### Run development web server (inside VM or on host)

`> scons run.server`

You can also use the standard `> ./manage.py runserver` command from Django, but this works only without Vagrant. Inside a Vagrant box, the command above adjusts the IP adress for the development server.

#### Run backend services (inside VM or on host)

`> scons run.backend`

## Writing tests for FuzzEd

`> scons fixture.save`

Saves a new fixture file from the current database. It can be referenced
in the unit tests stored in the tests directory.

`> scons run.tests`

Run all tests stored in the tests directory.

## Packaging FuzzEd

Please note that the machine were the packaging (and implicit build) takes place must be the same as the production machine. The smartest approach therefore is to develop in Vagrant with some distribution, and use then the same distro on the production host.

`> scons package.web`
`> scons package.backend`

## Acknowledgements

People who contributed to this project so far:

* Franz Becker      (analysis)
* Markus Götz       (core architecture, frontend)
* Lena Herscheid    (analysis, simulation)
* Felix Kubicek     (frontend)
* Stefan Richter    (frontend)
* Frank Schlegel    (core architecture, frontend)
* Christian Werling (frontend)