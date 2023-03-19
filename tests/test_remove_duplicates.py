import pytest


def generate_test_cases():
    yield from [
        (
            [
                (0, 1, "Hello"),
                (1, 2, "Hello"),
                (2, 3, "Hi"),
                (3, 4, "Bye"),
                (4, 5, "Bye"),
                (5, 6, "Bye"),
                (6, 7, "Good"),
                (7, 8, "Luck"),
                (8, 9, "Luck"),
            ],
            [
                (0, 2, "Hello"),
                (2, 3, "Hi"),
                (3, 6, "Bye"),
                (6, 7, "Good"),
                (7, 9, "Luck"),
            ],
        ),
        (
            [
                (0, 1, "Hello"),
                (1, 2, "Hello"),
                (2, 3, "Hello"),
                (3, 4, "Hello"),
                (4, 5, "Hello"),
                (5, 6, "Hello"),
            ],
            [(0, 6, "Hello")],
        ),
        (
            [
                (0, 1, "Hello"),
                (1, 2, "Hi"),
                (2, 3, "Bye"),
                (3, 4, "Good"),
                (4, 5, "Luck"),
            ],
            [
                (0, 1, "Hello"),
                (1, 2, "Hi"),
                (2, 3, "Bye"),
                (3, 4, "Good"),
                (4, 5, "Luck"),
            ],
        ),
        ([], []),
        (
            [
                (0, 1, "Hello"),
                (1, 2, "Hello"),
                (2, 3, "Hi"),
                (3, 4, "Bye"),
                (4, 5, "Bye"),
                (5, 6, "Hi"),
                (6, 7, "Hi"),
                (7, 8, "Hi"),
            ],
            [(0, 2, "Hello"), (2, 3, "Hi"), (3, 5, "Bye"), (5, 8, "Hi")],
        ),
    ]


@pytest.mark.parametrize("input_list, expected_output", generate_test_cases())
def test_remove_duplicates(sub, input_list, expected_output):
    instance = sub
    result = instance.remove_duplicates(input_list)
    print(result)
    assert result == expected_output
