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
      ~Subtitle.get_styles
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
      ~Subtitle.only_default_style
      ~Subtitle.include_styles
      ~Subtitle.exclude_styles

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

Style Filtering
--------------

List Available Styles
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from pyasstosrt import Subtitle

    # Get list of available styles
    sub = Subtitle('subtitle.ass')
    styles = sub.get_styles()
    print(f"Available styles: {styles}")

Export Only Default Styles
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from pyasstosrt import Subtitle

    # Export only dialogue styles (excludes signs, credits, etc.)
    sub = Subtitle('subtitle.ass', only_default_style=True)
    sub.export()

Include Specific Styles
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from pyasstosrt import Subtitle

    # Export only specific styles
    sub = Subtitle('subtitle.ass', include_styles=['Default', 'Alt'])
    sub.export()

    # Or as a single style
    sub = Subtitle('subtitle.ass', include_styles=['Default'])
    sub.export()

Exclude Specific Styles
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from pyasstosrt import Subtitle

    # Export all styles except specific ones
    sub = Subtitle('subtitle.ass', exclude_styles=['Signs', 'Credits'])
    sub.export()

    # Exclude multiple styles
    sub = Subtitle('subtitle.ass', exclude_styles=['Signs', 'Credits_dvd', 'Opening', 'Ending'])
    sub.export()

Combine Style Filtering with Other Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from pyasstosrt import Subtitle

    # Combine style filtering with effects removal
    sub = Subtitle(
        'subtitle.ass',
        only_default_style=True,
        removing_effects=True,
        remove_duplicates=True
    )
    sub.export('output')

    # Include specific styles with custom options
    sub = Subtitle(
        'subtitle.ass',
        include_styles=['Default', 'Thoughts'],
        removing_effects=True
    )
    sub.export('output', encoding='utf-8')

.. note::
   The style filtering options (``only_default_style``, ``include_styles``, ``exclude_styles``)
   are mutually exclusive. You can only use one at a time. If you try to use multiple,
   a ``ValueError`` will be raised.
