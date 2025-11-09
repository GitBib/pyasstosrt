import tempfile
from pathlib import Path

from pyasstosrt import Subtitle


def test_srt_empty_file():
    """Test handling of empty SRT file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".srt", delete=False, encoding="utf-8") as f:
        f.write("")
        temp_path = f.name

    try:
        sub = Subtitle(temp_path)
        sub.convert()
        # Empty file should result in no dialogues
        assert len(sub.dialogues) == 0
    finally:
        Path(temp_path).unlink()


def test_srt_only_whitespace():
    """Test handling of SRT file with only whitespace."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".srt", delete=False, encoding="utf-8") as f:
        f.write("\n\n   \n\t\n")
        temp_path = f.name

    try:
        sub = Subtitle(temp_path)
        sub.convert()
        assert len(sub.dialogues) == 0
    finally:
        Path(temp_path).unlink()


def test_srt_malformed_timecodes():
    """Test handling of malformed timecodes in SRT."""
    srt_content = """1
00:00:01,000 -> 00:00:03,000
This timecode is malformed

2
00:00:04,000 --> 00:00:06,000
This one is correct

"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".srt", delete=False, encoding="utf-8") as f:
        f.write(srt_content)
        temp_path = f.name

    try:
        sub = Subtitle(temp_path)
        sub.convert()
        # Should only parse the correctly formatted subtitle
        assert len(sub.dialogues) == 1
        assert sub.dialogues[0].text == "This one is correct"
    finally:
        Path(temp_path).unlink()


def test_srt_missing_text():
    """Test handling of subtitles without text."""
    srt_content = """1
00:00:01,000 --> 00:00:03,000

2
00:00:04,000 --> 00:00:06,000
This has text

3
00:00:07,000 --> 00:00:09,000


"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".srt", delete=False, encoding="utf-8") as f:
        f.write(srt_content)
        temp_path = f.name

    try:
        sub = Subtitle(temp_path)
        sub.convert()
        # Should only parse subtitles with text
        assert len(sub.dialogues) == 1
        assert sub.dialogues[0].text == "This has text"
    finally:
        Path(temp_path).unlink()


def test_srt_extra_blank_lines():
    """Test handling of extra blank lines between subtitles."""
    srt_content = """1
00:00:01,000 --> 00:00:03,000
First subtitle


2
00:00:04,000 --> 00:00:06,000
Second subtitle



3
00:00:07,000 --> 00:00:09,000
Third subtitle

"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".srt", delete=False, encoding="utf-8") as f:
        f.write(srt_content)
        temp_path = f.name

    try:
        sub = Subtitle(temp_path)
        sub.convert()
        assert len(sub.dialogues) == 3
        assert sub.dialogues[0].text == "First subtitle"
        assert sub.dialogues[1].text == "Second subtitle"
        assert sub.dialogues[2].text == "Third subtitle"
    finally:
        Path(temp_path).unlink()


def test_srt_non_sequential_numbers():
    """Test handling of non-sequential subtitle numbers."""
    srt_content = """1
00:00:01,000 --> 00:00:03,000
First subtitle

5
00:00:04,000 --> 00:00:06,000
Fifth subtitle

2
00:00:07,000 --> 00:00:09,000
Second subtitle

"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".srt", delete=False, encoding="utf-8") as f:
        f.write(srt_content)
        temp_path = f.name

    try:
        sub = Subtitle(temp_path)
        sub.convert()
        # Should parse all subtitles and sort by time
        assert len(sub.dialogues) == 3
        # After sorting by time, dialogues should be reindexed
        assert sub.dialogues[0].index == 1
        assert sub.dialogues[1].index == 2
        assert sub.dialogues[2].index == 3
    finally:
        Path(temp_path).unlink()


def test_srt_windows_line_endings():
    """Test handling of Windows-style line endings (CRLF)."""
    srt_content = (
        "1\r\n00:00:01,000 --> 00:00:03,000\r\nFirst subtitle\r\n\r\n"
        "2\r\n00:00:04,000 --> 00:00:06,000\r\nSecond subtitle\r\n"
    )

    with tempfile.NamedTemporaryFile(mode="w", suffix=".srt", delete=False, encoding="utf-8", newline="") as f:
        f.write(srt_content)
        temp_path = f.name

    try:
        sub = Subtitle(temp_path)
        sub.convert()
        assert len(sub.dialogues) == 2
        assert sub.dialogues[0].text == "First subtitle"
        assert sub.dialogues[1].text == "Second subtitle"
    finally:
        Path(temp_path).unlink()


def test_srt_special_characters():
    """Test handling of special characters in subtitle text."""
    srt_content = """1
00:00:01,000 --> 00:00:03,000
Special chars: <>&"'

2
00:00:04,000 --> 00:00:06,000
Unicode: 你好世界 Привет мир

"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".srt", delete=False, encoding="utf-8") as f:
        f.write(srt_content)
        temp_path = f.name

    try:
        sub = Subtitle(temp_path)
        sub.convert()
        assert len(sub.dialogues) == 2
        assert sub.dialogues[0].text == "Special chars: <>&\"'"
        assert "你好世界" in sub.dialogues[1].text
        assert "Привет мир" in sub.dialogues[1].text
    finally:
        Path(temp_path).unlink()


def test_srt_very_long_text():
    """Test handling of very long subtitle text."""
    long_text = "This is a very long subtitle. " * 50  # 1500+ characters

    srt_content = f"""1
00:00:01,000 --> 00:00:05,000
{long_text}

"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".srt", delete=False, encoding="utf-8") as f:
        f.write(srt_content)
        temp_path = f.name

    try:
        sub = Subtitle(temp_path)
        sub.convert()
        assert len(sub.dialogues) == 1
        assert len(sub.dialogues[0].text) > 1000
        assert "This is a very long subtitle." in sub.dialogues[0].text
    finally:
        Path(temp_path).unlink()
