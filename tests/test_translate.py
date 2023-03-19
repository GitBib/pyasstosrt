import os


def test_translate(sub):
    sub.export()
    with open("tests/sub.srt", 'r') as file:
        file1 = open("tests/sub_standard.srt", 'r')
        assert file.read() == file1.read()
    file1.close()
    os.remove("tests/sub.srt")
