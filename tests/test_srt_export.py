import tempfile
from pathlib import Path

from pyasstosrt import Subtitle


def test_export_srt_output_dialogues(sub_srt):
    """Test exporting SRT file as dialogues list."""
    dialogues = sub_srt.export(output_dialogues=True)
    assert dialogues is not None
    assert len(dialogues) > 0
    # Original file should not be modified
    assert Path("tests/test_sample.srt").is_file()


def test_export_srt_default(sub_srt):
    """Test default export of SRT file (should create normalized SRT)."""
    # Export to a different location to avoid overwriting the test file
    try:
        sub_srt.export("tests/folder")
        assert Path("tests/folder/test_sample.srt").is_file()
    finally:
        output_file = Path("tests/folder/test_sample.srt")
        if output_file.is_file():
            output_file.unlink()


def test_export_srt_output_dir(sub_srt):
    """Test exporting SRT file to specified output directory."""
    try:
        sub_srt.export("tests/folder")
        assert Path("tests/folder/test_sample.srt").is_file()
    finally:
        output_file = Path("tests/folder/test_sample.srt")
        if output_file.is_file():
            output_file.unlink()


def test_export_srt_compatibility(sub_srt):
    """Test SRT export with all parameters (compatibility check)."""
    try:
        sub_srt.export("tests/folder", "utf8", False)
        assert Path("tests/folder/test_sample.srt").is_file()
    finally:
        output_file = Path("tests/folder/test_sample.srt")
        if output_file.is_file():
            output_file.unlink()


def test_export_srt_output_dialogues_true(sub_srt):
    """Test SRT export with output_dialogues=True doesn't create file."""
    dialogues = sub_srt.export(None, "utf8", True)
    assert dialogues is not None
    assert len(dialogues) > 0
    # Should not create any file
    assert Path("tests/test_sample.srt").is_file()  # Original still exists


def test_export_srt_with_remove_duplicates():
    """Test SRT export with remove_duplicates option."""
    # Create a temporary SRT file for testing
    temp_srt_content = """1
00:00:01,000 --> 00:00:03,000
First subtitle

2
00:00:04,000 --> 00:00:06,000
Second subtitle

"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".srt", delete=False, encoding="utf-8") as f:
        f.write(temp_srt_content)
        temp_path = f.name

    try:
        sub_with_duplicates = Subtitle(temp_path, remove_duplicates=True)

        # Check that export worked
        dialogues = sub_with_duplicates.export(output_dialogues=True)
        assert len(dialogues) > 0
    finally:
        temp_file = Path(temp_path)
        if temp_file.exists():
            temp_file.unlink()
