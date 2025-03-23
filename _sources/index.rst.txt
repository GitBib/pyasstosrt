pyasstosrt
==========

Welcome to the pyasstosrt documentation! Here you will find information about the core functionality and examples of how to use the library.

Overview
--------

pyasstosrt is a Python library for converting Advanced SubStation Alpha (ASS/SSA) subtitle files to SubRip (SRT) format. It provides a simple and efficient way to transform subtitle files between these formats.

Main Features
-------------

- Convert ASS/SSA subtitles to SRT format
- Remove effects from subtitle text (optional)
- Remove and merge consecutive duplicate dialogues (optional)
- Support for both string paths and Path-like objects
- Command-line interface (CLI) for easy usage

Installation
------------

To install pyasstosrt from PyPI, use the following command:

.. code-block:: bash

    $ pip install 'pyasstosrt[cli]'

If you don't need the CLI functionality, you can install the library without extras:

.. code-block:: bash

    $ pip install pyasstosrt

For development purposes, you can clone the repository and install it in editable mode:

.. code-block:: bash

    $ git clone https://github.com/GitBib/pyasstosrt.git
    $ cd pyasstosrt
    $ pip install -e .

You can also run pyasstosrt without installation using ``uvx``:

.. code-block:: bash

    $ uvx --from 'pyasstosrt[cli]' pyasstosrt export * --remove-effects --remove-duplicates

Quick Start
-----------

Here's a basic example of how to use pyasstosrt:

.. code-block:: python

    from pyasstosrt import Subtitle

    # Convert a single file
    sub = Subtitle('subtitle.ass')
    sub.export()

    # Convert with effects removal
    sub = Subtitle('subtitle.ass', removing_effects=True)
    sub.export()

    # Convert with duplicate removal
    sub = Subtitle('subtitle.ass', remove_duplicates=True)
    sub.export()

    # Convert with custom output directory and encoding
    sub = Subtitle('subtitle.ass')
    sub.export(output_dir='output', encoding='utf-8')

Command Line Interface
--------------------

The library provides a command-line interface for easy usage:

.. code-block:: bash

    # Convert a single file
    pyasstosrt export subtitle.ass

    # Convert multiple files
    pyasstosrt export file1.ass file2.ass

    # Convert with effects removal
    pyasstosrt export subtitle.ass --remove-effects

    # Convert with duplicate removal
    pyasstosrt export subtitle.ass --remove-duplicates

    # Convert with custom output directory
    pyasstosrt export subtitle.ass --output-dir ./output

    # Convert with custom encoding
    pyasstosrt export subtitle.ass --encoding utf-8

    # Print dialogues to console
    pyasstosrt export subtitle.ass --output-dialogues

    # Run without installation using uvx
    uvx --from 'pyasstosrt[cli]' pyasstosrt export * --remove-effects --remove-duplicates

For more details on the CLI, see the :doc:`CLI documentation <pyasstosrt/cli>`.

Documentation
------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   pyasstosrt/cli
   pyasstosrt/batch_processing
   pyasstosrt/troubleshooting

API Reference
------------

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   pyasstosrt/subtitle
   pyasstosrt/dialogue
   pyasstosrt/time

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
