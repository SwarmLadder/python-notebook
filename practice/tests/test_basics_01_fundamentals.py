import math

import pytest

from practice_loader import module_for

m = module_for(__file__)


def test_total_cost():
    assert m.total_cost("2.50") == pytest.approx(17.5)
    assert m.total_cost(" 3 ", units=2) == pytest.approx(6.0)
    assert m.total_cost("0") == 0


def test_circle_measurements():
    area, circumference = m.circle_measurements(2)
    assert area == pytest.approx(4 * math.pi)
    assert circumference == pytest.approx(4 * math.pi)
    assert m.circle_measurements(0) == (0, 0)
    with pytest.raises(ValueError):
        m.circle_measurements(-1)


@pytest.mark.parametrize("minutes, expected", [(135, (2, 15)), (60, (1, 0)), (59, (0, 59)), (0, (0, 0))])
def test_split_minutes(minutes, expected):
    assert tuple(m.split_minutes(minutes)) == expected


def test_format_price():
    assert m.format_price("Coffee", 3.5) == "Coffee: $3.50"
    assert m.format_price("Tea", 2) == "Tea: $2.00"
    assert m.format_price("Cake", 4.999) == "Cake: $5.00"


def test_ends():
    assert m.ends("notebook") == ("note", "ook")
    assert m.ends("abc") == ("abc", "abc"), "short strings: slicing never raises IndexError"


@pytest.mark.parametrize("raw, expected", [("  HeLLo ", "hello"), ("Straße", "strasse"), ("", "")])
def test_normalize(raw, expected):
    assert m.normalize(raw) == expected


def test_hyphenate():
    assert m.hyphenate("learn  python   today") == "learn-python-today"
    assert m.hyphenate("single") == "single"


@pytest.mark.parametrize("name, expected", [("data.csv", True), ("DATA.CSV", True), ("data.csv.bak", False), ("csv", False)])
def test_is_csv(name, expected):
    assert m.is_csv(name) is expected


@pytest.mark.parametrize("score, expected", [(0, True), (100, True), (50.5, True), (-0.1, False), (100.1, False)])
def test_is_valid_score(score, expected):
    assert m.is_valid_score(score) is expected


def test_fahrenheit_to_celsius():
    assert m.fahrenheit_to_celsius(72.5) == 22.5
    assert m.fahrenheit_to_celsius(32) == 0
    assert m.fahrenheit_to_celsius(-40) == -40


def test_parse_order():
    quantities, total = m.parse_order("apple:2:0.50, bread:1:2.25,milk:3:1.10")
    assert quantities == {"apple": 2, "bread": 1, "milk": 3}
    assert total == pytest.approx(6.55)
