def test_translate(sub):
    sub.translate()
    file = open("tests/sub.srt", 'r')
    file1 = open("tests/sub_standard.srt", 'r')
    assert file.read() == file1.read()
