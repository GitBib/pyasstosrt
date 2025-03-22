from pathlib import Path

import pytest

from pyasstosrt import Subtitle


def test_open():
    path = "tests/sub.ass"
    sub = Subtitle(path)
    assert sub


def test_open_use_pathlib():
    path = Path("tests/sub.ass")
    sub = Subtitle(path)
    assert sub


@pytest.mark.parametrize(
    "file_path, expected_error",
    [
        ("tests/sub.ass", TypeError),
        ("tests/", FileNotFoundError),
        ("tests/sub1.ass", FileNotFoundError),
    ],
)
def test_open_errors(file_path, expected_error):
    if expected_error is TypeError:
        with open(file_path, "r") as file:
            with pytest.raises(expected_error):
                Subtitle(file)
    else:
        with pytest.raises(expected_error):
            Subtitle(file_path)
