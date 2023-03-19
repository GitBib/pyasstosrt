import pytest
import sys
import os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f'{myPath}/../')

from pyasstosrt import Subtitle


@pytest.fixture
def sub():
    return Subtitle('tests/sub.ass')
