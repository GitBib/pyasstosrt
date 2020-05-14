pyasstosrt
=================================================================================================================================================================================

![alt text](https://api.travis-ci.com/GitBib/pyasstosrt.svg?branch=master) [![alt text](https://img.shields.io/pypi/v/pyasstosrt.svg?style=flat)](https://pypi.org/project/pyasstosrt/)

**pyasstosrt** – this tool will help you convert Advanced SubStation Alpha (ASS/SSA) subtitle files to SubRip (SRT) files.

```python
from pyasstosrt import Subtitle

sub = Subtitle('sub.ass')
sub.export()
```

Installation
------------
    $ pip install pyasstosrt
