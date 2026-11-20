import pytest

from practice_loader import module_for

m = module_for(__file__)


@pytest.mark.parametrize("temp, label", [(-5, "freezing"), (0, "freezing"), (0.1, "cold"), (14.9, "cold"),
                                          (15, "comfortable"), (24.9, "comfortable"), (25, "hot")])
def test_classify_temperature(temp, label):
    assert m.classify_temperature(temp) == label


@pytest.mark.parametrize("n, expected", [(15, True), (30, True), (0, True), (9, False), (10, False), (7, False)])
def test_divisible_by_3_and_5(n, expected):
    assert m.divisible_by_3_and_5(n) is expected


@pytest.mark.parametrize("args", [(1, 2, 3), (3, 2, 1), (2, 3, 1), (5, 5, 5), (-1, -7, -3)])
def test_greatest_of_three(args):
    assert m.greatest_of_three(*args) == max(args)


@pytest.mark.parametrize("score, grade", [(100, "A"), (90, "A"), (89.9, "B"), (80, "B"), (70, "C"), (60, "D"), (59, "F"), (0, "F")])
def test_letter_grade(score, grade):
    assert m.letter_grade(score) == grade


@pytest.mark.parametrize("bad", [-1, 101])
def test_letter_grade_rejects_out_of_range(bad):
    with pytest.raises(ValueError):
        m.letter_grade(bad)


@pytest.mark.parametrize("password, ok", [("abcdefg1", True), ("abcdefgh", False), ("abc1", False), ("12345678", True)])
def test_is_valid_password(password, ok):
    assert m.is_valid_password(password) is ok


def test_is_valid_password_custom_length():
    assert m.is_valid_password("ab1", min_length=3)


@pytest.mark.parametrize("n, total", [(0, 0), (1, 1), (10, 55), (100, 5050)])
def test_sum_to(n, total):
    assert m.sum_to(n) == total


@pytest.mark.parametrize("n, result", [(0, 1), (1, 1), (5, 120), (10, 3628800)])
def test_factorial(n, result):
    assert m.factorial(n) == result


def test_factorial_negative():
    with pytest.raises(ValueError):
        m.factorial(-1)


def test_count_vowels():
    assert m.count_vowels("Programming in PYTHON") == 5
    assert m.count_vowels("rhythm") == 0
    assert m.count_vowels("") == 0


def test_first_above():
    assert m.first_above([5, 101, 200]) == 101
    assert m.first_above([100, 50]) is None, "100 is not *greater* than 100"
    assert m.first_above([], limit=0) is None
    assert m.first_above([1, 2, 3], limit=1) == 2


def test_first_above_stops_early():
    def values():
        yield 150
        raise AssertionError("kept looping after finding the answer — use return or break")
    assert m.first_above(values()) == 150


def test_count_signs():
    assert m.count_signs([3, -1, 0, 7, 0]) == {"positive": 2, "negative": 1, "zero": 2}
    assert m.count_signs([]) == {"positive": 0, "negative": 0, "zero": 0}


def test_triangle():
    assert m.triangle(3) == "*\n**\n***"
    assert m.triangle(1) == "*"
    assert m.triangle(0) == ""


def test_multiples_of_seven():
    assert m.multiples_of_seven(4) == [7, 14, 21, 28]
    assert m.multiples_of_seven(0) == []


def test_fizzbuzz():
    result = m.fizzbuzz(50)
    assert len(result) == 50
    assert result[:5] == ["1", "2", "Fizz", "4", "Buzz"]
    assert result[14] == "FizzBuzz"
    assert result[44] == "FizzBuzz"
    assert result[49] == "Buzz"
