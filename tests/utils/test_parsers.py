import pytest

from app.utils.parser import format_number, parse_float, parse_int


@pytest.mark.parametrize(
    "value, expected",
    [
        ("123.45", 123.45),
        ("123,45", 123.45),
        ("  123,45  ", 123.45),
        ("abc", 0.0),
        ("", 0.0),
        ("  ", 0.0),
    ],
)
def test_parse_float(value: str, expected: float) -> None:
    assert parse_float(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        ("123", 123),
        (" 123 ", 123),
        ("abc", 0),
        ("12.3", 0),
        ("", 0),
        ("  ", 0),
    ],
)
def test_parse_int(value: str, expected: int) -> None:
    assert parse_int(value) == expected


@pytest.mark.parametrize(
    "number, expected",
    [
        (123.4567, "123,46"),
        (0.0, "0,00"),
        (1.0, "1,00"),
        (1.234, "1,23"),
        (99.999, "100,00"),
    ],
)
def test_format_number(number: float, expected: str) -> None:
    assert format_number(number) == expected
