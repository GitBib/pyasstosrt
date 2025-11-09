from pathlib import Path


def test_export_output_dialogues(sub):
    assert sub.export(output_dialogues=True)
    assert not Path("tests/sub.srt").is_file()


def test_export_default(sub):
    try:
        sub.export()
        assert Path("tests/sub.srt").is_file()
    finally:
        output_file = Path("tests/sub.srt")
        if output_file.is_file():
            output_file.unlink()


def test_export_output_dir(sub):
    try:
        sub.export("tests/folder")
        assert Path("tests/folder/sub.srt").is_file()
    finally:
        output_file = Path("tests/folder/sub.srt")
        if output_file.is_file():
            output_file.unlink()


def test_export_compatibility(sub):
    try:
        sub.export("tests/folder", "utf8", False)
        assert Path("tests/folder/sub.srt").is_file()
    finally:
        output_file = Path("tests/folder/sub.srt")
        if output_file.is_file():
            output_file.unlink()


def test_export_output_dialogues_true(sub):
    assert sub.export(None, "utf8", True)
    assert not Path("tests/sub.srt").is_file()
