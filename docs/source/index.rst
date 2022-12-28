.. SimpleSecurity documentation master file, created by
   sphinx-quickstart on Wed Dec 28 09:18:45 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
.. image:: ../../readme-assets/icons/name.png
   :width: 700
   :alt: Project Icon

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


Overview
========

Combine multiple popular python security tools and generate reports or output
into different formats. Each tool is organized around the idea of a plugin. Plugins (these require the plugin
executable in the system path. e.g. bandit requires bandit to be in the system path...) Current plugins include:

- bandit
- safety
- dodgy
- dlint (flake8)
- semgrep
- Trivy
- Black (for code formatting)

The output of the scans is standardized and the tool can print to stdOut as well as write the results to a file. Output
formats include:

- ansi (for terminal)
- json
- markdown
- csv
- sarif

Lastly, this tool enables annotations for PR in GitHub. This means that code-checking can be done easily and that the
results are written as annotations in the GitHub PR. Example GitHub Actions are also provided.

.. toctree::
   :hidden:
   :caption: Docs
   :maxdepth: 4

   self
   gettingstarted
   changelog
   license
   security
   support
   codeOfConduct
   contribution
   rationale

.. toctree::
   :hidden:
   :caption: API
   :maxdepth: 4

   modules


.. toctree::
   :caption: Misc
   :maxdepth: 4
   :hidden:

   genindex
   modindex
   search