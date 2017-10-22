[![Build Status](https://travis-ci.org/troeger/fuzzed.svg?branch=master)](https://travis-ci.org/troeger/fuzzed)

# ORE - The Open Reliability Editor (former FuzzEd)

Note: FuzzEd becomes ORE. We are in the middle of that process, so don't get confused while both names are still in use.

ORE is an browser-based editor for drawing and analyzing dependability models. The currently supported types are:

* Fault Tree Diagrams
* FuzzTree Diagrams
* Reliability Block Diagrams
* Data Flow Diagrams

The editor supports the following generic features for all diagram types:

* Organization of diagrams in projects, per user.
* Sharing of (read-only) graphs between users of the same installation. We use that heavily for education scenarios.
* Creation of diagram snapshots.
* Full clipboard functionality inside the editor.
* LaTEX, PDF and EPS export for some diagram types.
* GraphML export for all diagram types.
* Analytical and simulation-based analysis of fault tree and FuzzTree diagrams. 
* REST API for creating new diagrams with external software.

You can try the editor at http://fuzzed.org.

## Local installation

Currently not supported. Use http://fuzzed.org or wait for https://github.com/troeger/fuzzed/issues/107 to be finished.

## Development

Thanks for your interest in this project. We would love to have you on-board. There is some information in the [Wiki](https://github.com/troeger/fuzzed/wiki/Home). The developers discuss in the [ORE forum](https://groups.google.com/forum/#!forum/ore-dev).

The only tested environment for development, at the moment, is a virtual machine managed by Vagrant. On your machine, you need:

  * VirtualBox 5.1.30
  * Vagrant 1.9.8
  * Ansible 2.1.1.0
  
Other versions of these three products may work, too.
  
Get a checkout of the master, or the latest release tag, and run ``vagrant up``. This takes a while and installs you a development and execution environment for frontend and backend in a virtual machine.

When this was successful, the next step is to enter the VM and to run SCons for building all static parts of the project:

    vagrant ssh
    scons frontend backend

If this was successful, you need to initialize the database (SQLite by default):

    ./manage.py migrate

Now you can start the development web server:

    ./manage.py runserver

From this point, you should be able to use the frontend on your machine. Use the URL http://vagrant.fuzzed.org:8000, which points to the local address of the Vagrant machine on your computer. 

With a second SSH login into the machine, you can also have analysis and simulation services available by running:

    scons run.backend 

Please check the [architecture description](https://github.com/troeger/fuzzed/wiki/FuzzEdArchitecture) description page for further details.

The start page should have a *Developer Login* link right below the OAuth login logos, which works without Internet connectivity.  The OAuth login logos are broken by default, since you need [OAuth2 credentials](https://github.com/troeger/fuzzed/wiki/OAuth2Cred) to be configured for that.

If your working on a staging machine, a valid option is to get an OpenID from somewhere such as https://openid.stackexchange.com.

### Development without Vagrant

Our setup is only tested on Ubuntu Trusty 32-bit, as installed by Vagrant. The software dependencies are mostly likely to break on other platforms. You have been warned ...

After cloning the repository, run the following command:

    ansible-playbook -i ansible/inventories/localhost ansible/dev.yml 

The next steps are as above. The only new thing is the environment variable DJANGO_CONFIGURATION, which is automatically set in the Vagrant case:

    export DJANGO_CONFIGURATION=Dev
    scons frontend backend
    ./manage.py migrate 
    ./manage.py runserver 
    ... Coding ...

## Prepare and run a production machine from a checkout

    scons frontend backend
    scons package
    ansible-playbook -i ansible/inventories/localhost -e release_version=0.X.X ansible/prod_fe.yml
    ansible-playbook -i ansible/inventories/localhost -e release_version=0.X.X ansible/prod_be.yml

We store our private credentials (OAuth keys etc.) for the fuzzed.org installation in an Ansible vault.
If you do the same, don't forget to add the *--ask-vault-pass* option to the line above.

## Licence

FuzzEd ist licensed under the [GNU AGPL Version 3](http://en.wikipedia.org/wiki/Affero_General_Public_License). This means your are allowed to:

* Install and run the unmodified FuzzEd code at your site.
* Re-package and distribute the unmodified version of FuzzEd from this repository. 
* Fork and re-publish the editor, as long as your modified sources are accessible for everybody.

In short, AGPL forbids you to distribute or run your own modified version of FuzzEd without publishing your code.
 
## Acknowledgements

People who contributed to this project so far:

* Franz Becker      (analysis)
* Markus Götz       (core architecture, frontend)
* Lena Herscheid    (analysis, simulation)
* Felix Kubicek     (frontend)
* Stefan Richter    (frontend)
* Frank Schlegel    (core architecture, frontend)
* Christian Werling (frontend)
