import os
from os.path import isfile


def test_export(sub):
    # Check output_dialogues
    assert sub.export(output_dialogues=True)
    assert not isfile("tests/sub.srt")

    # Checking the default export
    sub.export()
    assert isfile("tests/sub.srt")
    os.remove("tests/sub.srt")

    # Checking output_dir
    sub.export("tests/folder")
    assert isfile("tests/folder/sub.srt")
    os.remove("tests/folder/sub.srt")

    # Checking compatibility
    sub.export("tests/folder", "utf8", False)
    assert isfile("tests/folder/sub.srt")
    os.remove("tests/folder/sub.srt")

    assert sub.export(None, "utf8", True)
    assert not isfile("tests/sub.srt")
