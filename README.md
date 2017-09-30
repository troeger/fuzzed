[![Build Status](https://travis-ci.org/troeger/fuzzed.svg?branch=master)](https://travis-ci.org/troeger/fuzzed)

# FuzzEd

FuzzEd is an browser-based editor for drawing and analyzing dependability models. The currently supported types are:

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

## Installation

Currently not supported. Use http://fuzzed.org or wait for https://github.com/troeger/fuzzed/issues/107 to be finished.

## Development

If you want to contribute to FuzzEd, there is a lot of information in the [Wiki](https://github.com/troeger/fuzzed/wiki/Home).

For the impatient, you just need a checkout, Ubuntu and Ansible:

### Prepare and run a development machine from a checkout

* ansible-playbook -i ansible/inventories/localhost ansible/dev.yml
* scons frontend backend
* ./manage.py migrate --configuration=Dev
* ./manage.py runserver --configuration=Dev
* ... Coding ...
* Update the version number in FuzzEd/__init__.py
* scons package

### Prepare and run a production machine from a checkout

* scons frontend backend
* scons package
* ansible-playbook -i ansible/inventories/localhost -e release_version=0.X.X ansible/prod_fe.yml
* ansible-playbook -i ansible/inventories/localhost -e release_version=0.X.X ansible/prod_be.yml

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
