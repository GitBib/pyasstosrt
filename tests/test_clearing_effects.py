import os
from pathlib import Path

from pyasstosrt import Subtitle


def test_removing_effects():
    path = Path('tests/sub-removing-effects.ass')
    sub = Subtitle(path, removing_effects=True)
    sub.export()
    file = open("tests/sub-removing-effects.srt", 'r')
    file1 = open("tests/sub_standard-removing-effects.srt", 'r')
    assert file.read() == file1.read()
    os.remove("tests/sub-removing-effects.srt")
