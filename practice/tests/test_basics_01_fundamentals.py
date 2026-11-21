import pytest

from grader import check
from practice_loader import module_for

m = module_for(__file__)


@pytest.mark.parametrize("price_text, units", [("2.50", 7), (" 3 ", 2), ("0", 7), ("19.99", 1)])
def test_total_cost(price_text, units):
    check(m.total_cost(price_text, units))


def test_total_cost_default_units():
    check(m.total_cost("1.25"), hint="units defaults to 7")

    assert m.total_cost("2.50", 0) == 0, "A zero-unit order costs zero."


@pytest.mark.parametrize("radius", [0, 1, 2.5])
def test_circle_measurements(radius):
    check(m.circle_measurements(radius))


def test_circle_measurements_rejects_negative():
    with pytest.raises(ValueError):
        m.circle_measurements(-1)


@pytest.mark.parametrize("minutes", [135, 60, 59, 0, 1441])
def test_split_minutes(minutes):
    check(m.split_minutes(minutes))


@pytest.mark.parametrize("product, price", [("Coffee", 3.5), ("Tea", 2), ("Cake", 4.999)])
def test_format_price(product, price):
    check(m.format_price(product, price), hint="always two decimal places")


@pytest.mark.parametrize("text", ["notebook", "abc", "python"])
def test_ends(text):
    check(m.ends(text), hint="short strings must not raise IndexError")


@pytest.mark.parametrize("raw", ["  HeLLo ", "Straße", "", "\tMiXeD case\n"])
def test_normalize(raw):
    check(m.normalize(raw))


@pytest.mark.parametrize("sentence", ["learn  python   today", "single", ""])
def test_hyphenate(sentence):
    check(m.hyphenate(sentence))


@pytest.mark.parametrize("name", ["data.csv", "DATA.CSV", "data.csv.bak", "csv", "report.Csv"])
def test_is_csv(name):
    check(m.is_csv(name))


@pytest.mark.parametrize("score", [0, 100, 50.5, -0.1, 100.1])
def test_is_valid_score(score):
    check(m.is_valid_score(score), hint="both ends are included")


@pytest.mark.parametrize("fahrenheit", [72.5, 32, -40, 212])
def test_fahrenheit_to_celsius(fahrenheit):
    check(m.fahrenheit_to_celsius(fahrenheit))


def test_parse_order():
    check(m.parse_order("apple:2:0.50, bread:1:2.25,milk:3:1.10"))
    check(m.parse_order("tea:1:3"), hint="a single entry has no comma")


@pytest.mark.parametrize("name", ["ada  lovelace", "Guido van Rossum", "", "x"])
def test_initials(name):
    check(m.initials(name))


@pytest.mark.parametrize("seconds", [3725, 0, 59, 86399])
def test_clock_time(seconds):
    check(m.clock_time(seconds))


@pytest.mark.parametrize("text", ["Racecar", "A man, a plan, a canal: Panama!", "python", "", "ab"])
def test_is_palindrome(text):
    check(m.is_palindrome(text))


@pytest.mark.parametrize("old, new", [(50, 75), (80, 60), (3, 3), (7, 10)])
def test_percent_change(old, new):
    check(m.percent_change(old, new))


def test_percent_change_from_zero():
    with pytest.raises(ValueError):
        m.percent_change(0, 5)


@pytest.mark.parametrize("number", ["1234 5678 9012 3456", "4321", "12345"])
def test_mask_card(number):
    check(m.mask_card(number))
