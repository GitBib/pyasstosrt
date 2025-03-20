Time
====

.. currentmodule:: pyasstosrt

.. autoclass:: Time
   :members:
   :undoc-members:
   :show-inheritance:
   :inherited-members:

   .. rubric:: Methods

   .. autosummary::
      :nosignatures:
      :toctree: _autosummary

      ~Time.__init__
      ~Time.__sub__
      ~Time.__str__

   .. rubric:: Attributes

   .. autosummary::
      :nosignatures:
      :toctree: _autosummary

      ~Time.hour
      ~Time.minute
      ~Time.second
      ~Time.millisecond

   .. rubric:: Examples

   Basic usage:

   .. code-block:: python

      from pyasstosrt import Time

      # Create time objects
      time1 = Time("1:23:45.67")
      time2 = Time("0:00:10.00")

      # Access components
      print(time1.hour)      # 1
      print(time1.minute)    # 23
      print(time1.second)    # 45
      print(time1.millisecond)  # 670

      # Calculate duration
      duration = time1 - time2
      print(duration)  # 5023.67 (seconds)

      # Convert to string (SRT format)
      print(str(time1))  # 01:23:45,670
      print(str(time2))  # 00:00:10,000
