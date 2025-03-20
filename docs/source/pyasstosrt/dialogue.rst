Dialogue
========

.. currentmodule:: pyasstosrt

.. autoclass:: Dialogue
   :members:
   :undoc-members:
   :show-inheritance:
   :inherited-members:

   .. rubric:: Methods

   .. autosummary::
      :nosignatures:
      :toctree: _autosummary

      ~Dialogue.get_timestamp
      ~Dialogue.__str__

   .. rubric:: Attributes

   .. autosummary::
      :nosignatures:
      :toctree: _autosummary

      ~Dialogue.index
      ~Dialogue.start
      ~Dialogue.end
      ~Dialogue.text

   .. rubric:: Examples

   Basic usage:

   .. code-block:: python

      from pyasstosrt import Dialogue, Time

      # Create a dialogue entry
      dialogue = Dialogue(
          index=1,
          start="0:00:10.00",
          end="0:00:15.00",
          text="Hello, world!"
      )

      # Get timestamp
      timestamp = dialogue.get_timestamp()
      print(timestamp)  # 00:00:10,000 --> 00:00:15,000

      # Convert to string (SRT format)
      srt_format = str(dialogue)
      print(srt_format)
      # 1
      # 00:00:10,000 --> 00:00:15,000
      # Hello, world!
