import os
import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

from pyasstosrt import Subtitle

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f"{myPath}/../")


@pytest.fixture
def sub():
    return Subtitle("tests/sub.ass")


@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.fixture
def test_dir():
    return Path("tests")


@pytest.fixture
def test_files(test_dir):
    return {
        "sub": test_dir / "sub.ass",
        "sub_removing_effects": test_dir / "sub-removing-effects.ass",
        "sub_standard": test_dir / "sub_standard.srt",
        "sub_standard_removing_effects": test_dir / "sub_standard-removing-effects.srt",
    }


@pytest.fixture
def cleanup_srt_files(test_files):
    srt_files = {
        "sub": test_files["sub"].with_suffix(".srt"),
        "sub_removing_effects": test_files["sub_removing_effects"].with_suffix(".srt"),
    }

    for file in srt_files.values():
        if file.exists():
            file.unlink()

    yield

    for file in srt_files.values():
        if file.exists():
            file.unlink()


@pytest.fixture
def output_dir(tmp_path):
    output_dir = tmp_path / "output"
    output_dir.mkdir(exist_ok=True)
    return output_dir


@pytest.fixture
def invalid_ass_file(tmp_path):
    invalid_file = tmp_path / "invalid.ass"
    content = "This is not a valid ASS file"
    invalid_file.write_text(content, encoding="utf-8")
    return invalid_file, content
