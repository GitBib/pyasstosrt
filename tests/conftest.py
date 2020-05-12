import pytest
from pathlib import Path
from pyasstosrt import Subtitle


@pytest.fixture
def sub():
    file = Path('tests/sub.ass').read_text(encoding="utf8")
    sub = Subtitle(file)
    return sub
