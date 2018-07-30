Quickstart
==========

Requirements
------------

This module has no requirements. The *requirements.dev.txt* is for development to the module only and contains packages
like Sphinx and setuptools.

Installation
------------

Install the package using the following command.

.. code-block:: bash

    pip install grigori

Example
-------

The simple example below watches the current directory for any changes, and notifies us of the file and type of the
change.

For more detailed usage please see the :ref:`usage-documentation`

.. code-block:: python

    from grigori import Watcher

    directory = './'

    w = Watcher(directory)

    for changes in w.watch():
        for change in changes:
            print("file '%s' has been changed in the following way: '%s'" % (change["file"], change["type"]))