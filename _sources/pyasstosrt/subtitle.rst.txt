Subtitle
========

.. currentmodule:: pyasstosrt

.. autoclass:: Subtitle
   :members:
   :undoc-members:
   :show-inheritance:
   :inherited-members:

   .. rubric:: Methods

   .. autosummary::
      :nosignatures:
      :toctree: _autosummary

      ~Subtitle.convert
      ~Subtitle.export
      ~Subtitle.get_text
      ~Subtitle.remove_duplicates
      ~Subtitle.subtitle_formatting
      ~Subtitle.text_clearing
      ~Subtitle.merged_dialogues

   .. rubric:: Attributes

   .. autosummary::
      :nosignatures:
      :toctree: _autosummary

      ~Subtitle.filepath
      ~Subtitle.file
      ~Subtitle.raw_text
      ~Subtitle.dialogues
      ~Subtitle.removing_effects
      ~Subtitle.is_remove_duplicates

   .. rubric:: Examples

   Basic usage:

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

      # Get dialogues without exporting
      sub = Subtitle('subtitle.ass')
      dialogues = sub.export(output_dialogues=True)

Examples
--------

Basic Usage
----------

.. code-block:: python

    from pyasstosrt import Subtitle

    # Convert ASS/SSA file to SRT
    sub = Subtitle(filepath='input.ass')
    sub.convert()
    sub.export()

    # Access dialogues
    for dialogue in sub.dialogues:
        print(f"{dialogue.start} -> {dialogue.end}: {dialogue.text}")

Advanced Usage
-------------

.. code-block:: python

    from pyasstosrt import Subtitle

    # Convert with options
    sub = Subtitle(
        filepath='input.ass',
        removing_effects=True,
        remove_duplicates=True
    )
    sub.convert()
    sub.export('output/directory', encoding='utf-8')
