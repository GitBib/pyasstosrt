import pytest
import sys
import os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from pyasstosrt import Subtitle


@pytest.fixture
def sub():
    sub = Subtitle('tests/sub.ass')
    return sub
