import pytest


@pytest.mark.parametrize(
    "raw_text, expected_text",
    [
        ("  Hello, world!  ", "Hello, world!"),
        (r"Hello\hworld!", "Hello\xa0world!"),
        (r"Hello\Nworld!", "Hello\nworld!"),
        (r"  Hello\hworld!\NThis\his\ha\htest.  ", "Hello\xa0world!\nThis\xa0is\xa0a\xa0test."),
    ],
)
def test_text_clearing(sub, raw_text, expected_text):
    cleared_text = sub.text_clearing(raw_text)
    assert cleared_text == expected_text
