import pytest
import sys
import os
from pyasstosrt import Subtitle

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')


@pytest.fixture
def sub():
    sub = Subtitle('tests/sub.ass')
    return sub
