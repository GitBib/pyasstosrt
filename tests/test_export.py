import os
from os.path import isfile


def test_export_output_dialogues(sub):
    assert sub.export(output_dialogues=True)
    assert not isfile("tests/sub.srt")


def test_export_default(sub):
    try:
        sub.export()
        assert isfile("tests/sub.srt")
    finally:
        if isfile("tests/sub.srt"):
            os.remove("tests/sub.srt")


def test_export_output_dir(sub):
    try:
        sub.export("tests/folder")
        assert isfile("tests/folder/sub.srt")
    finally:
        if isfile("tests/folder/sub.srt"):
            os.remove("tests/folder/sub.srt")


def test_export_compatibility(sub):
    try:
        sub.export("tests/folder", "utf8", False)
        assert isfile("tests/folder/sub.srt")
    finally:
        if isfile("tests/folder/sub.srt"):
            os.remove("tests/folder/sub.srt")


def test_export_output_dialogues_true(sub):
    assert sub.export(None, "utf8", True)
    assert not isfile("tests/sub.srt")
