# FuzzEd

## Preparation of development machine

The recommend development mode is with Vagrant. The Vagrantfile installs all relevant stuff in the virtual machine. Inside the Vagrant VM, you can find all sources at /home/fuzztrees. Just install Vagrant and run:

`vagrant up`

If you prefer to develop on your native machine without any virtualization, it needs Python, PIP and Ansible  (version 1.6 or higher is required). Then run:

`ansible-playbook -i ansible/dev_machine ansible/site.yml`

Add a "-s" option if you have a password-less 'sudo' available instead of working in your root account. Our Ansible code is prepared for Linux and Mac OS X development machines.

## Developing for FuzzEd

### Compile static stuff                              

`> fab build.all`

Synchronize local database with current model:     > ./manage.py syncdb --migrate
Run development web server (inside VM or on host): > fab run.server
Run backend services (inside VM or on host):       > fab run.backend

## Writing tests for FuzzEd
> fab fixture_save:testgraphs.json

Saves a new fixture file from the current database. It can be referenced
in the unit tests stored in tests.py.

> fab fixture_load:testgraphs.json

Overwrites the current database with the test fixture. This allows local
editing of the test database with the editor, which can than be saved again.

> fab run_tests

Run all tests stored in tests.py.

## Deploying FuzzEd

Please note that the machine were the packaging (and implicit build) takes place must be the same as the production machine. The smartest approach therefore is to develop in Vagrant with some distribution, and use then the same distro on the production host.

> fab package.web
> fab package.backend
> fab deploy.web
> fab.deploy.backend

## Acknowledgements

People who contributed to this project so far:

Franz Becker      (analysis)
Markus Götz       (core architecture, frontend)
Lena Herscheid    (analysis, simulation)
Felix Kubicek     (frontend)
Stefan Richter    (frontend)
Frank Schlegel    (core architecture, frontend)
Christian Werling (frontend)