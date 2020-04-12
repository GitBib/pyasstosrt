def test_text_clearing(sub):
    raw_text = r"It's almost time for the fight!"
    done_text = r"It's almost time for the fight!"
    text_test = sub.text_clearing(raw_text)
    assert text_test == done_text
