import pytest

from pyasstosrt import Substation


@pytest.fixture
def sub():
    sub = Substation('tests/sub.ass')
    return sub
