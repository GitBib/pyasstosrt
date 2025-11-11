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

You can get a list of all styles in the file and filter subtitles by style names.

```python
from pyasstosrt import Subtitle

# Get list of all styles in the file
sub = Subtitle('sub.ass')
styles = sub.get_styles()
print(styles)  # ['Default', 'Alt', 'Signs', 'Credits']

# Export only styles with "Default" in name (e.g., Default, Default_dvd)
sub = Subtitle('sub.ass', only_default_style=True)
sub.export()

# Export only Default style
sub = Subtitle('sub.ass', include_styles=['Default'])
sub.export()

# Export only Default and Alt styles
sub = Subtitle('sub.ass', include_styles=['Default', 'Alt'])
sub.export()

# Exclude Signs and Credits styles
sub = Subtitle('sub.ass', exclude_styles=['Signs', 'Credits'])
sub.export()
```

CLI
------------

### 🎬 Export Command

Convert ASS/SSA subtitle files to SRT format with various options.

**Basic usage:**
```bash
pyasstosrt export subtitle.ass
```

**Specify output directory:**
```bash
pyasstosrt export subtitle.ass --output-dir /path/to/output
# or use short form
pyasstosrt export subtitle.ass -o /path/to/output
```

**Remove effects and duplicates:**
```bash
pyasstosrt export subtitle.ass --remove-effects --remove-duplicates
# or use short form
pyasstosrt export subtitle.ass -r -d
```

**Process multiple files at once:**
```bash
pyasstosrt export subtitle1.ass subtitle2.ass subtitle3.ass
```

**Style filtering options:**
```bash
# Export only styles with "Default" in name (e.g., Default, Default_dvd)
pyasstosrt export subtitle.ass --only-default

# Export only specific styles
pyasstosrt export subtitle.ass --include-styles "Default,Signs"

# Exclude specific styles
pyasstosrt export subtitle.ass --exclude-styles "Signs,Credits"
```

**Custom encoding:**
```bash
pyasstosrt export subtitle.ass --encoding utf-16
```

**Print dialogues to console:**
```bash
pyasstosrt export subtitle.ass --output-dialogues
```

### 🎨 Styles Command

List all unique styles found in an ASS subtitle file.

**Basic usage:**
```bash
pyasstosrt styles subtitle.ass
```

**Display in table format:**
```bash
pyasstosrt styles subtitle.ass --table
# or use short form
pyasstosrt styles subtitle.ass -t
```

### 🔧 General Options

**Show version:**
```bash
pyasstosrt --version
# or
pyasstosrt -v
```

**Show help:**
```bash
pyasstosrt --help
pyasstosrt export --help
pyasstosrt styles --help
```

**Enable shell completion:**
```bash
# For bash
pyasstosrt --install-completion bash

# For zsh
pyasstosrt --install-completion zsh

# For fish
pyasstosrt --install-completion fish
```

Installation
------------
Most users will want to simply install the latest version, hosted on PyPI:

    $ pip install 'pyasstosrt[cli]'

If you just want to use it as a library and don't need the CLI, you can omit the `[cli]` extra.
