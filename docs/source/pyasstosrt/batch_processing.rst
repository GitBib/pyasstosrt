Batch Processing
===============

PyAssToSrt provides multiple ways to batch process subtitle files. This guide demonstrates various approaches for processing multiple files at once.

Using the Command Line Interface
--------------------------------

The simplest way to process multiple files is using the CLI:

.. code-block:: bash

    pyasstosrt export file1.ass file2.ass file3.ass

You can also use glob patterns through your shell:

.. code-block:: bash

    pyasstosrt export ./subtitles/*.ass

All CLI options are applied to every file being processed:

.. code-block:: bash

    pyasstosrt export ./subtitles/*.ass --remove-effects --remove-duplicates --output-dir ./output

Using Python Script
------------------

For more complex scenarios, you can write a Python script to process files:

Basic Batch Processing
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import glob
    from pathlib import Path
    from pyasstosrt import Subtitle

    # Get all ASS files in a directory
    ass_files = glob.glob("./subtitles/*.ass")

    # Process each file
    for file_path in ass_files:
        try:
            sub = Subtitle(file_path)
            sub.export(output_dir="./output")
            print(f"Converted: {file_path}")
        except Exception as e:
            print(f"Error converting {file_path}: {e}")

Advanced Batch Processing
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import os
    from pathlib import Path
    from concurrent.futures import ThreadPoolExecutor
    from pyasstosrt import Subtitle

    def process_file(file_path, remove_effects=False, remove_duplicates=False):
        try:
            sub = Subtitle(
                file_path, 
                removing_effects=remove_effects,
                remove_duplicates=remove_duplicates
            )
            output_path = Path("./output") / Path(file_path).stem
            sub.export(output_dir=output_path)
            return f"Success: {file_path}"
        except Exception as e:
            return f"Error: {file_path} - {str(e)}"

    # Get all ASS files recursively
    def get_all_ass_files(root_dir):
        ass_files = []
        for root, _, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".ass"):
                    ass_files.append(os.path.join(root, file))
        return ass_files

    # Process files in parallel
    def batch_process(directory, max_workers=4):
        ass_files = get_all_ass_files(directory)
        os.makedirs("./output", exist_ok=True)
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(
                process_file, 
                ass_files,
                [True] * len(ass_files),  # remove_effects=True for all files
                [True] * len(ass_files)   # remove_duplicates=True for all files
            ))
        
        for result in results:
            print(result)

    if __name__ == "__main__":
        batch_process("./subtitles")

Custom Processing Logic
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from pathlib import Path
    from pyasstosrt import Subtitle

    def custom_process(file_path, output_dir):
        # Read ASS file
        sub = Subtitle(file_path)
        
        # Perform conversion
        sub.convert()
        
        # Custom processing - filter dialogues
        filtered_dialogues = []
        for dialogue in sub.dialogues:
            # Example: Keep only dialogues longer than 2 seconds
            duration = dialogue.end - dialogue.start
            if duration > 2.0:
                filtered_dialogues.append(dialogue)
        
        # Replace original dialogues with filtered ones
        sub.dialogues = filtered_dialogues
        
        # Export the result
        sub.export(output_dir=output_dir)

    # Process a file with custom logic
    custom_process("./subtitles/file.ass", "./output")

Tips and Best Practices
----------------------

1. **Error Handling**: Always include error handling to prevent the entire batch from failing if one file has issues.

2. **Output Organization**: Consider organizing output files in a structured way, especially for large batches.

3. **Progress Reporting**: For large batches, add progress reporting to track the conversion process.

4. **Performance**: Use parallel processing for large batches, but be mindful of system resources.

5. **Validation**: Consider adding validation of the converted SRT files to ensure they meet your requirements. 