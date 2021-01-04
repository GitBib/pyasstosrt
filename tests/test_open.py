from pyasstosrt import Subtitle
from pathlib import Path


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
    try:
        Subtitle(file)
        assert False
    except TypeError:
        assert True


def test_open_folder():
    try:
        Subtitle('tests/')
        assert False
    except FileNotFoundError:
        assert True


def test_open_broken_file():
    try:
        Subtitle('tests/sub1.ass')
        assert False
    except FileNotFoundError:
        assert True
