import pytest
from pyasstosrt import Subtitle


@pytest.fixture
def sub():
    sub = Subtitle('tests/sub.ass')
    return sub
