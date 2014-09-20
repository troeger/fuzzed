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

You can try the editor at http://www.fuzzed.org.

## Installation

If you just want to install your own copy of FuzzEd, please read the [installation guide](https://github.com/troeger/fuzzed/wiki/InstallationGuide).

## Development

If you want to contribute to FuzzEd, there is a lot of information in the [Wiki](https://github.com/troeger/fuzzed/wiki/Home).

The developers hang around on the [dev mailing list](mailto:fuzzed@lists.nclmail.de).

## Licence

FuzzEd ist licensed under the AGPL Version 3. This means your are allowed to:

* Install and run the unmodified FuzzEd code at your site.
* Re-package and distribute the unmodified version of FuzzEd from this repository. 
* Modify and re-publish (fork) the editor, as long as your modified sources are accessible for everybody.

In short, AGPL forbids you to distribute / run your own modified version of FuzzEd without publishing your code.
 
## Acknowledgements

People who contributed to this project so far:

* Franz Becker      (analysis)
* Markus Götz       (core architecture, frontend)
* Lena Herscheid    (analysis, simulation)
* Felix Kubicek     (frontend)
* Stefan Richter    (frontend)
* Frank Schlegel    (core architecture, frontend)
* Christian Werling (frontend)
