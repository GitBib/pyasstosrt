from pathlib import Path


def test_translate(sub):
    sub.export()
    with open("tests/sub.srt", "r") as file:
        file1 = open("tests/sub_standard.srt", "r")
        assert file.read() == file1.read()
    file1.close()
    Path("tests/sub.srt").unlink()
