import pytest

from pyasstosrt import Time


def test_negative_sub_time():
    time_1 = Time("01:23:09.73")
    time_2 = Time("01:22:09.73")
    sub = time_1 - time_2
    assert sub == 60.0


def test_same_time_sub():
    time_1 = Time("01:23:09.73")
    time_2 = Time("01:23:09.73")
    sub = time_2 - time_1
    assert sub == 0.0


def test_millisecond_sub():
    time_1 = Time("01:23:09.73")
    time_2 = Time("01:23:09.75")
    sub = time_2 - time_1
    assert sub == 0.02


@pytest.mark.parametrize("input_time, expected_output", [
    ("0:00:00.00", "00:00:00,000"),
    ("0:01:00.00", "00:01:00,000"),
    ("1:23:45.67", "01:23:45,670"),
    ("12:34:56.78", "12:34:56,780"),
])
def test_str_conversion(input_time, expected_output):
    t = Time(input_time)
    assert str(t) == expected_output
