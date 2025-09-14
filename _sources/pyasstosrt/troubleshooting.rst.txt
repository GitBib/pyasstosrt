Troubleshooting
==============

This guide covers common issues that may arise when using pyasstosrt and how to solve them.

Installation Issues
-----------------

CLI Tools Not Found
~~~~~~~~~~~~~~~~~

**Problem**: After installing pyasstosrt, the CLI command isn't available.

**Solution**: Make sure you installed the package with the CLI extras:

.. code-block:: bash

    pip install 'pyasstosrt[cli]'

If you've already installed without the extras, you can upgrade your installation:

.. code-block:: bash

    pip install --upgrade 'pyasstosrt[cli]'

Dependency Conflicts
~~~~~~~~~~~~~~~~~

**Problem**: You encounter dependency conflicts when installing pyasstosrt.

**Solution**: Try installing in a virtual environment:

.. code-block:: bash

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install 'pyasstosrt[cli]'

File Conversion Issues
--------------------

File Not Found
~~~~~~~~~~~~

**Problem**: You get a `FileNotFoundError` when trying to convert a file.

**Solution**: Check that the file path is correct. Use absolute paths or ensure you're in the right directory:

.. code-block:: python

    from pathlib import Path
    import os

    # Using absolute path
    abs_path = os.path.abspath("./subtitles/file.ass")
    sub = Subtitle(abs_path)

    # Or using pathlib
    file_path = Path("./subtitles/file.ass").resolve()
    sub = Subtitle(file_path)

Incorrect Format
~~~~~~~~~~~~~

**Problem**: The converted SRT file has incorrect formatting or timing.

**Solution**: Check that your ASS file follows the standard format. If the issue persists, try to:

1. Open the ASS file in a text editor to verify it has the correct structure
2. Check for any unusual formatting in the ASS file
3. Try converting with removing effects enabled:

.. code-block:: python

    sub = Subtitle("file.ass", removing_effects=True)
    sub.export()

Missing Text
~~~~~~~~~~

**Problem**: Some dialogues are missing in the converted SRT file.

**Solution**: This might happen if dialogues have empty text or only contain effects. Try:

1. Convert without removing effects:

.. code-block:: python

    sub = Subtitle("file.ass", removing_effects=False)
    sub.export()

2. Check the original ASS file for empty dialogues

Encoding Issues
~~~~~~~~~~~~

**Problem**: The converted file has garbled text or incorrect characters.

**Solution**: Specify the correct encoding for the output file:

.. code-block:: python

    # For Cyrillic subtitles
    sub.export(encoding="utf-8")  # or "cp1251" for Windows Cyrillic

    # For other languages
    sub.export(encoding="utf-16")  # or other appropriate encoding

If the problem persists, check the encoding of your source ASS file and make sure your system supports the required encodings.

CLI Specific Issues
----------------

Multiple Files Not Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem**: When using glob patterns with the CLI, not all files are processed.

**Solution**: Your shell might not be expanding the glob pattern correctly. Try either:

1. Use quotes around the pattern:

.. code-block:: bash

    pyasstosrt export "./subtitles/*.ass"

2. Or list files explicitly:

.. code-block:: bash

    pyasstosrt export file1.ass file2.ass file3.ass

Performance Issues
---------------

Slow Batch Processing
~~~~~~~~~~~~~~~~~~

**Problem**: Processing many files is slow.

**Solution**: Use parallel processing as shown in the batch processing guide:

.. code-block:: python

    from concurrent.futures import ThreadPoolExecutor

    # Process files in parallel
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(process_file_function, file_list)

Debugging
--------

Debug Common Issues
~~~~~~~~~~~~~~~~~

When troubleshooting, it's often helpful to add print statements to see what's happening:

.. code-block:: python

    sub = Subtitle("file.ass")

    # Print raw text from the file
    print(sub.raw_text[:500])  # First 500 chars

    # Print found dialogues after conversion
    sub.convert()
    print(f"Found {len(sub.dialogues)} dialogues")

    # Print the first dialogue
    if sub.dialogues:
        print(f"First dialogue: {sub.dialogues[0]}")

Getting Help
----------

If you encounter an issue not covered in this guide:

1. Check the project's GitHub repository for open and closed issues
2. Open a new issue on GitHub with details of your problem
3. Include sample code and if possible, a sample ASS file to reproduce the issue
