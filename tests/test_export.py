import os
from os.path import isfile


def test_export(sub):
    sub.export()
    assert isfile("tests/sub.srt")
    os.remove("tests/sub.srt")
    sub.export("tests/folder")
    assert isfile("tests/folder/sub.srt")
    os.remove("tests/folder/sub.srt")
