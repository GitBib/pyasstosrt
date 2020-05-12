from pyasstosrt import Time


def test_time():
    t = Time("01:23:09.73")
    assert t.second == 9
    assert t.minute == 23
    assert t.hour == 1
    assert t.millisecond == 73
    assert str(t) == '01:23:09,73'
