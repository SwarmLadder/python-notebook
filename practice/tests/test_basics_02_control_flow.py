import pytest

from grader import check
from practice_loader import module_for

m = module_for(__file__)


@pytest.mark.parametrize("temp", [-5, 0, 0.1, 14.9, 15, 24.9, 25, 40])
def test_classify_temperature(temp):
    check(m.classify_temperature(temp), hint="check each boundary: is it < or <=?")


@pytest.mark.parametrize("n", [15, 30, 0, 9, 10, 7, -45])
def test_divisible_by_3_and_5(n):
    check(m.divisible_by_3_and_5(n))


@pytest.mark.parametrize("args", [(1, 2, 3), (3, 2, 1), (2, 3, 1), (5, 5, 5), (-1, -7, -3)])
def test_greatest_of_three(args):
    assert m.greatest_of_three(*args) == max(args)


@pytest.mark.parametrize("score", [100, 90, 89.9, 80, 70, 60, 59, 0])
def test_letter_grade(score):
    check(m.letter_grade(score))


@pytest.mark.parametrize("bad", [-1, 101])
def test_letter_grade_rejects_out_of_range(bad):
    with pytest.raises(ValueError):
        m.letter_grade(bad)


@pytest.mark.parametrize("password", ["abcdefg1", "abcdefgh", "abc1", "12345678", ""])
def test_is_valid_password(password):
    check(m.is_valid_password(password))


def test_is_valid_password_custom_length():
    check(m.is_valid_password("ab1", min_length=3))


@pytest.mark.parametrize("n", [0, 1, 10, 100])
def test_sum_to(n):
    check(m.sum_to(n))


@pytest.mark.parametrize("n", [0, 1, 5, 10])
def test_factorial(n):
    check(m.factorial(n))


def test_factorial_negative():
    with pytest.raises(ValueError):
        m.factorial(-1)


@pytest.mark.parametrize("text", ["Programming in PYTHON", "rhythm", "", "AEIOU aeiou"])
def test_count_vowels(text):
    check(m.count_vowels(text), hint="uppercase vowels count too")


@pytest.mark.parametrize("values, limit", [([5, 101, 200], 100), ([100, 50], 100), ([], 0), ([1, 2, 3], 1)])
def test_first_above(values, limit):
    check(m.first_above(values, limit), hint="strictly greater; None when nothing qualifies")


def test_first_above_stops_early():
    def values():
        yield 150
        raise AssertionError("kept looping after finding the answer — use return or break")
    m.first_above(values())


@pytest.mark.parametrize("values", [[3, -1, 0, 7, 0], [], [-2, -2]])
def test_count_signs(values):
    check(m.count_signs(values))


@pytest.mark.parametrize("rows", [3, 1, 0])
def test_triangle(rows):
    check(m.triangle(rows))


@pytest.mark.parametrize("n", [4, 0, 1])
def test_multiples_of_seven(n):
    check(m.multiples_of_seven(n))


def test_fizzbuzz():
    result = m.fizzbuzz(50)
    assert len(result) == 50, "one entry per number 1..n"
    check(result)
    assert m.fizzbuzz(0) == []


@pytest.mark.parametrize("year", [2024, 2023, 1900, 2000, 2100])
def test_is_leap_year(year):
    check(m.is_leap_year(year), hint="centuries are special")


@pytest.mark.parametrize("n", [472, -472, 0, 9, 1001])
def test_digit_sum(n):
    check(m.digit_sum(n))


@pytest.mark.parametrize("n", [1, 2, 6, 27])
def test_collatz_steps(n):
    check(m.collatz_steps(n))


def test_collatz_rejects_zero():
    with pytest.raises(ValueError):
        m.collatz_steps(0)


@pytest.mark.parametrize("limit", [1, 2, 30, 100])
def test_primes_up_to(limit):
    check(m.primes_up_to(limit))


@pytest.mark.parametrize("rows", [3, 1, 0])
def test_number_pyramid(rows):
    check(m.number_pyramid(rows))
