.. SimpleSecurity documentation master file, created by
   sphinx-quickstart on Wed Dec 28 09:18:45 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to SimpleSecurity's documentation!
==========================================
.. image:: https://img.shields.io/github/languages/top/FHPythonUtils/SimpleSecurity.svg?style=for-the-badge)](../../)
   :alt: GitHub top language

.. image:: https://img.shields.io/github/repo-size/FHPythonUtils/SimpleSecurity.svg?style=for-the-badge)](../../)
   :alt: Repository size

.. image:: https://img.shields.io/github/issues/FHPythonUtils/SimpleSecurity.svg?style=for-the-badge)](../../issues)
   :alt: Issues

.. image:: https://img.shields.io/github/license/FHPythonUtils/SimpleSecurity.svg?style=for-the-badge)](/LICENSE.md)
   :alt: License

.. image:: https://img.shields.io/github/commit-activity/m/FHPythonUtils/SimpleSecurity.svg?style=for-the-badge)](../../commits/master)
   :alt: Commit activity

.. image:: https://img.shields.io/github/last-commit/FHPythonUtils/SimpleSecurity.svg?style=for-the-badge)](../../commits/master)
   :alt: Last commit

.. image:: https://img.shields.io/pypi/dm/simplesecurity.svg?style=for-the-badge)](https://pypistats.org/packages/simplesecurity)
   :alt: PyPI Downloads

.. image:: https://img.shields.io/badge/dynamic/json?style=for-the-badge&label=total%20downloads&query=%24.total_downloads&url=https%3A%2F%2Fapi.pepy.tech%2Fapi%2Fprojects%2Fsimplesecurity)](https://pepy.tech/project/simplesecurity)
   :alt: PyPI Total Downloads

.. image:: https://img.shields.io/pypi/v/simplesecurity.svg?style=for-the-badge)](https://pypi.org/project/simplesecurity)
   :alt: PyPI Version

.. image:: ../../readme-assets/icons/name.png
   :width: 600
   :alt: Project Icon

Overview
========

Combine multiple popular python security tools and generate reports or output
into different formats

Plugins (these require the plugin executable in the system path. e.g. bandit
requires bandit to be in the system path...)
   - bandit
   - safety
   - dodgy
   - dlint
   - semgrep

Formats
   - ansi (for terminal)
   - json
   - markdown
   - csv
   - sarif

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   _apidocs/modules

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Getting Started
===============

Install With PIP
----------------
A requirement for using SimpleSecurity is having a version of python 3.x installed.

.. highlight:: bash
.. code-block:: bash

   pip install simplesecurity



Head to https://pypi.org/project/SimpleSecurity/ for more info
This program has been written for Python versions 3.7 - 3.10 and has been tested with both 3.7 and
3.10

Run CLI
---------
In order to run the CLI utility, you can run `simplesecurity` in this directory

.. image:: ../../readme-assets/screenshots/sec.svg
   :width: 500px
   :alt: Screenshot

Options in the CLI tool include:

.. highlight:: bash
.. code-block:: bash

   usage: __main__.py [-h] [--format FORMAT] [--plugin PLUGIN] [--file FILE]
                      [--level LEVEL] [--confidence CONFIDENCE]
                      [--no-colour] [--high-contrast] [--fast] [--zero]

   Combine multiple popular python security tools...

   and generate reports or output into different formats.

   optional arguments:
     -h, --help            show this help message and exit
     --format FORMAT, -f FORMAT
                           Output format. One of ansi, json, markdown, csv. default=ansi
     --plugin PLUGIN, -p PLUGIN
                           Plugin to use. One of bandit, safety, dodgy, dlint, semgrep, all, default=all
     --file FILE, -o FILE  Filename to write to (omit for stdout)
     --level LEVEL, -l LEVEL
                           Minimum level/ severity to show
     --confidence CONFIDENCE, -c CONFIDENCE
                           Minimum confidence to show
     --no-colour, -z       No ANSI colours
     --high-contrast, -Z   High contrast colours
     --fast, --skip        Skip long running jobs. Will omit plugins with long run time (applies to -p all only)
     --zero, -0            Return non zero exit code if any security vulnerabilities are found


You can also import this into your own project and use any of the functions
in the DOCS

Configuring Semgrep
-------------------
The configuration of SemGrep is organized with a `yaml` file. A default config is already enclosed in this library. I
you want to specify the config, you can follow the steps below:

1. Clone https://github.com/returntocorp/semgrep-rules
2. cd to `semgrep-rules/python`
3. do

.. highlight:: bash
.. code-block:: bash

   cat **/security/**/*.yaml >> semgrep_sec.yaml
   cat **/security/*.yaml >> semgrep_sec.yaml


4. Find and replace `rules:` with `` apart from the first instance
5. Reformat with `ctrl+shift+i`
6. replace simplesecurity/semgrep_sec.yaml with the new one

Licence
=======

MIT License
Copyright (c) FredHappyface
(See the `LICENSE <../../../../LICENSE.md>`_ for more information.)

Changelog
=========

See the `Changelog </CHANGELOG.md>`_ for more information.

Code of Conduct
===============

Online communities include people from many backgrounds. The *Project*
contributors are committed to providing a friendly, safe and welcoming
environment for all. Please see the
`Code of Conduct <https://github.com/FHPythonUtils/.github/blob/master/CODE_OF_CONDUCT.md>`_ for more information.

Contributing
============

Contributions are welcome, please see the
`Contributing Guidelines <https://github.com/FHPythonUtils/.github/blob/master/CONTRIBUTING.md>`_ for more information.

Security
========

Thank you for improving the security of the project, please see the
`Security Policy <https://github.com/FHPythonUtils/.github/blob/master/SECURITY.md>`_
for more information.

Support
=======

Thank you for using this project, I hope it is of use to you. Please be aware that
those involved with the project often do so for fun along with other commitments
(such as work, family, etc). Please see the
`Support Policy <https://github.com/FHPythonUtils/.github/blob/master/SUPPORT.md>`_
for more information.

Rationale
=========

The rationale acts as a guide to various processes regarding projects such as
the versioning scheme and the programming styles used. Please see the
`Rationale <https://github.com/FHPythonUtils/.github/blob/master/RATIONALE.md>`_
for more information.
