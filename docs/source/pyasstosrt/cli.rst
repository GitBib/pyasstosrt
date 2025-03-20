Command Line Interface
=====================

PyAssToSrt provides a command-line interface (CLI) for easy batch conversion of ASS subtitle files. The CLI is available when you install the package with the `cli` extra:

.. code-block:: bash

    pip install 'pyasstosrt[cli]'

Basic Usage
----------

The basic command syntax is:

.. code-block:: bash

    pyasstosrt export [OPTIONS] FILEPATH...

Where `FILEPATH...` is one or more paths to ASS subtitle files.

Options
-------

The CLI supports the following options:

``--remove-effects, -r``
    Remove effects from subtitles.

``--remove-duplicates, -d``
    Remove duplicate subtitles.

``--output-dir, -o PATH``
    Output directory for the SRT file(s).

``--encoding, -e TEXT``
    Encoding for the output file. Default is "utf8".

``--output-dialogues, -p``
    Print dialogues to console.

``--version, -v``
    Show version and exit.

Examples
--------

Basic Conversion
~~~~~~~~~~~~~~~

Convert a single ASS file to SRT:

.. code-block:: bash

    pyasstosrt export subtitle.ass

Running Without Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can run pyasstosrt without installing it using tools like ``uvx``:

.. code-block:: bash

    uvx --from 'pyasstosrt[cli]' pyasstosrt export * --remove-effects --remove-duplicates

This command will use all ASS files in the current directory, remove effects and duplicates, and convert them to SRT format.

Convert Multiple Files
~~~~~~~~~~~~~~~~~~~~

Process multiple files at once:

.. code-block:: bash

    pyasstosrt export file1.ass file2.ass file3.ass

Remove Effects
~~~~~~~~~~~~

Convert and remove visual effects from the subtitle text:

.. code-block:: bash

    pyasstosrt export subtitle.ass --remove-effects

Remove Duplicates
~~~~~~~~~~~~~~~

Convert and remove/merge consecutive duplicate dialogues:

.. code-block:: bash

    pyasstosrt export subtitle.ass --remove-duplicates

Custom Output Directory
~~~~~~~~~~~~~~~~~~~~

Save the converted file(s) to a specific directory:

.. code-block:: bash

    pyasstosrt export subtitle.ass --output-dir ./output_folder

Custom Encoding
~~~~~~~~~~~~~

Specify the encoding for the output file:

.. code-block:: bash

    pyasstosrt export subtitle.ass --encoding utf-16

Print Dialogues
~~~~~~~~~~~~~

Convert and print the dialogues to the console:

.. code-block:: bash

    pyasstosrt export subtitle.ass --output-dialogues

Combine Options
~~~~~~~~~~~~~

You can combine multiple options:

.. code-block:: bash

    pyasstosrt export subtitle.ass --remove-effects --remove-duplicates --output-dir ./output
