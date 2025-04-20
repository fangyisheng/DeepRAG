def add(x, y):
    return x + y


def multiply(x, y):
    return x * y


import pytest


def test_add_positive_numbers():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-2, -3) == -5


@pytest.mark.parametrize(
    "x, y, expected",
    [
        (2, 3, 6),
        (-2, 3, -6),
        (0, 5, 0),
    ],
)
def test_multiply(x, y, expected):
    assert multiply(x, y) == expected


def test_add_string():
    with pytest.raises(TypeError):
        add("hello", 1)
