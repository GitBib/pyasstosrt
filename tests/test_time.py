from pyasstosrt import Time


def test_time():
    t = Time("01:23:09.73")
    assert t.second == 9
    assert t.minute == 23
    assert t.hour == 1
    assert t.millisecond == 730
    assert str(t) == '01:23:09,730'


def test_sub_time():
    time_1 = Time("01:23:09.73")
    time_2 = Time("01:24:09.73")
    sub = time_2.__sub__(time_1)
    assert sub == 60.0
    assert type(sub) == float
