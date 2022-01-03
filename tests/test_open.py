from pathlib import Path

import pytest

from pyasstosrt import Subtitle


def test_open():
    path = 'tests/sub.ass'
    sub = Subtitle(path)
    assert sub


def test_open_use_pathlib():
    path = Path('tests/sub.ass')
    sub = Subtitle(path)
    assert sub


def test_open_use_object():
    file = open('tests/sub.ass', 'r')
    with pytest.raises(TypeError):
        Subtitle(file)


def test_open_folder():
    with pytest.raises(FileNotFoundError):
        Subtitle('tests/')


def test_open_broken_file():
    with pytest.raises(FileNotFoundError):
        Subtitle('tests/sub1.ass')
