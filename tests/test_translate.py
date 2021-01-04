import os


def test_translate(sub):
    sub.export()
    file = open("tests/sub.srt", 'r')
    file1 = open("tests/sub_standard.srt", 'r')
    assert file.read() == file1.read()
    file.close()
    file1.close()
    os.remove("tests/sub.srt")
