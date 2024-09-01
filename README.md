pyasstosrt
=================================================================================================================================================================================

[![Downloads](https://pepy.tech/badge/pyasstosrt)](https://pepy.tech/project/pyasstosrt) [![codecov](https://codecov.io/gh/GitBib/pyasstosrt/branch/master/graph/badge.svg?token=VGTJ3NYHOV)](https://codecov.io/gh/GitBib/pyasstosrt)

**pyasstosrt** – this tool will help you convert Advanced SubStation Alpha (ASS/SSA) subtitle files to SubRip (SRT) files.

Support for str path:
```python
from pyasstosrt import Subtitle

sub = Subtitle('sub.ass')
sub.export()
```

Support for all Path-like objects, instead of only pathlib's Path:

```python
from pathlib import Path

from pyasstosrt import Subtitle

path = Path('sub.ass')
sub = Subtitle(path)
sub.export()
```

You can get a sheet with dialogue by specifying output_dialogues.

```python
from pathlib import Path

from pyasstosrt import Subtitle

path = Path('sub.ass')
sub = Subtitle(path)
sub.export(output_dialogues=True)
```

If you want to remove effects from text, you can use the removing_effects.

```python
from pyasstosrt import Subtitle

sub = Subtitle('sub.ass', removing_effects=True)
sub.export()
```

You can enable the deletion of duplicate lines with the rearrangement of start and end times.

```python
from pyasstosrt import Subtitle

sub = Subtitle('sub.ass', remove_duplicates=True)
sub.export()
```
CLI
------------
```bash
pyasstosrt export /Users/user/sub/sub.ass
```

**Optional** You can specify an export folder.
```bash
pyasstosrt export /Users/user/sub/sub.ass --output-dir /Users/user/sub/srt
```

**Optional** If you want to remove effects from text, you can use the --remove-effects flag.
```bash
pyasstosrt export /Users/user/sub/sub.ass --remove-effects --output-dir /Users/user/sub/srt
```

**Optional**  If you need to remove duplicates, you can use the --remove-duplicates flag.
```bash
pyasstosrt export /Users/user/sub/sub.ass --remove-duplicates
```

**Optional**  You can use the flags together --remove-duplicates --remove-effects
```bash
pyasstosrt export /Users/user/sub/sub.ass --remove-duplicates --remove-effects
```
Installation
------------
Most users will want to simply install the latest version, hosted on PyPI:

    $ pip install 'pyasstosrt[cli]'

If you just want to use it as a library and don't need the CLI, you can omit the `[cli]` extra.
