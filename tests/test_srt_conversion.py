import os
import tempfile

from pyasstosrt import Subtitle
from pyasstosrt.pyasstosrt import Subtitle as SubtitleClass


def test_srt_time_conversion():
    """Test SRT time format conversion to ASS format."""
    # SRT: 00:00:10,580 -> ASS: 0:00:10.58
    assert SubtitleClass._srt_time_to_ass("00:00:10,580") == "0:00:10.58"
    assert SubtitleClass._srt_time_to_ass("00:01:23,456") == "0:01:23.45"
    assert SubtitleClass._srt_time_to_ass("01:23:45,678") == "1:23:45.67"
    assert SubtitleClass._srt_time_to_ass("12:34:56,789") == "12:34:56.78"


def test_srt_dialogue_count(sub_srt):
    """Test that correct number of dialogues are parsed from SRT."""
    sub_srt.convert()
    # The test_sample.srt file has 5 dialogues
    assert len(sub_srt.dialogues) == 5


def test_srt_first_dialogue(sub_srt):
    """Test first dialogue is parsed correctly."""
    sub_srt.convert()
    first_dialogue = sub_srt.dialogues[0]

    assert first_dialogue.index == 1
    assert str(first_dialogue.start) == "00:00:10,580"
    assert str(first_dialogue.end) == "00:00:13,040"
    assert first_dialogue.text == "It's time for the main event!"


def test_srt_last_dialogue(sub_srt):
    """Test last dialogue is parsed correctly."""
    sub_srt.convert()
    last_dialogue = sub_srt.dialogues[-1]

    assert last_dialogue.index == 5
    assert "rivalry" in last_dialogue.text.lower()


def test_srt_text_extraction(sub_srt):
    """Test text extraction from SRT dialogues."""
    sub_srt.convert()

    # Check some known dialogue texts exist
    dialogue_texts = [d.text for d in sub_srt.dialogues]
    assert "It's time for the main event!" in dialogue_texts
    assert "Animal Mask vs. Macadamian Ogre, AKA, MAO!" in dialogue_texts


def test_srt_multiline_text():
    """Test parsing of multiline subtitles in SRT format."""
    # Create a simple SRT file with multiline text
    srt_content = """1
00:00:01,000 --> 00:00:03,000
First line
Second line

2
00:00:04,000 --> 00:00:06,000
Single line

"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".srt", delete=False, encoding="utf-8") as f:
        f.write(srt_content)
        temp_path = f.name

    try:
        sub = Subtitle(temp_path)
        sub.convert()

        assert len(sub.dialogues) == 2
        # Multiline text is joined with space
        assert sub.dialogues[0].text == "First line Second line"
        assert sub.dialogues[1].text == "Single line"
    finally:
        os.unlink(temp_path)


def test_srt_format_detection():
    """Test that SRT format is correctly detected."""
    sub_srt = Subtitle("tests/test_sample.srt")
    assert sub_srt.is_srt_format() is True

    sub_ass = Subtitle("tests/sub.ass")
    assert sub_ass.is_srt_format() is False


def test_srt_sorted_dialogues():
    """Test that dialogues are sorted by time."""
    sub_srt = Subtitle("tests/test_sample.srt")
    sub_srt.convert()

    # Check that dialogues are in chronological order
    # We can compare Time objects by converting to total seconds
    for i in range(len(sub_srt.dialogues) - 1):
        current = sub_srt.dialogues[i]
        next_dialogue = sub_srt.dialogues[i + 1]

        # Check that current starts before next
        current_start_seconds = (
            current.start.hour * 3600
            + current.start.minute * 60
            + current.start.second
            + current.start.millisecond / 1000
        )
        next_start_seconds = (
            next_dialogue.start.hour * 3600
            + next_dialogue.start.minute * 60
            + next_dialogue.start.second
            + next_dialogue.start.millisecond / 1000
        )
        assert current_start_seconds <= next_start_seconds


def test_srt_dialogue_structure(sub_srt):
    """Test that dialogue objects have correct structure."""
    sub_srt.convert()

    for dialogue in sub_srt.dialogues:
        # Each dialogue should have all required attributes
        assert hasattr(dialogue, "index")
        assert hasattr(dialogue, "start")
        assert hasattr(dialogue, "end")
        assert hasattr(dialogue, "text")

        # Index should be positive
        assert dialogue.index > 0

        # Text should not be empty
        assert len(dialogue.text) > 0

        # Start should be before end (using subtraction since Time supports it)
        duration = dialogue.end - dialogue.start
        assert duration > 0
