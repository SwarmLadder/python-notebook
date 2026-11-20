# Auto-graded practice. Replace each `raise NotImplementedError` with your code.
# Check your work:  python -m pytest practice -k basics_02_control_flow
# Stuck? Re-read the docstring hint, then the lesson notebook it names.
# Reset to a blank copy:  git checkout -- practice/exercises/basics_02_control_flow.py

"""Basics practice 2 — Control flow (if/elif/else, for, while, break).

Companion to basics/exercises/02_control_flow_exercises.ipynb and lessons 05–06.
"""


def classify_temperature(celsius: float) -> str:
    """Return 'freezing' (<= 0), 'cold' (< 15), 'comfortable' (< 25) or 'hot'.

    Hint: test the most restrictive condition first, then use elif.
    """
    raise NotImplementedError('TODO: implement classify_temperature')


def divisible_by_3_and_5(number: int) -> bool:
    """True when number is divisible by both 3 and 5."""
    raise NotImplementedError('TODO: implement divisible_by_3_and_5')


def greatest_of_three(a: float, b: float, c: float) -> float:
    """Return the largest value using comparisons only (do not call max())."""
    raise NotImplementedError('TODO: implement greatest_of_three')


def letter_grade(score: float) -> str:
    """Return 'A' (>= 90), 'B' (>= 80), 'C' (>= 70), 'D' (>= 60) or 'F'.

    Raise ValueError when score is outside 0–100.
    """
    raise NotImplementedError('TODO: implement letter_grade')


def is_valid_password(password: str, min_length: int=8) -> bool:
    """True if the password has at least min_length characters AND at least one digit.

    Hint: any(character.isdigit() for character in password)
    """
    raise NotImplementedError('TODO: implement is_valid_password')


def sum_to(n: int) -> int:
    """Sum the integers 1..n with a for loop over range(). sum_to(0) is 0."""
    raise NotImplementedError('TODO: implement sum_to')


def factorial(n: int) -> int:
    """Compute n! with a while loop. 0! is 1. Raise ValueError for negative n."""
    raise NotImplementedError('TODO: implement factorial')


def count_vowels(text: str) -> int:
    """Count a, e, i, o, u in text, ignoring case."""
    raise NotImplementedError('TODO: implement count_vowels')


def first_above(values: list[float], limit: float=100):
    """Return the first value greater than limit, or None if there is none.

    Hint: return (or break) as soon as you find it — no need to check the rest.
    """
    raise NotImplementedError('TODO: implement first_above')


def count_signs(values: list[float]) -> dict[str, int]:
    """Return {'positive': ..., 'negative': ..., 'zero': ...} counts."""
    raise NotImplementedError('TODO: implement count_signs')


def triangle(rows: int) -> str:
    """Return a left-aligned triangle of asterisks, one row per line.

    >>> print(triangle(3))
    *
    **
    ***
    """
    raise NotImplementedError('TODO: implement triangle')


def multiples_of_seven(n: int) -> list[int]:
    """Return the first n multiples of 7: [7, 14, 21, ...]."""
    raise NotImplementedError('TODO: implement multiples_of_seven')


def fizzbuzz(n: int) -> list[str]:
    """Return FizzBuzz for 1..n as strings: 'Fizz' (3), 'Buzz' (5), 'FizzBuzz' (both), else the number."""
    raise NotImplementedError('TODO: implement fizzbuzz')


def is_leap_year(year: int) -> bool:
    """Leap years are divisible by 4, except centuries, unless divisible by 400."""
    raise NotImplementedError('TODO: implement is_leap_year')


def digit_sum(n: int) -> int:
    """Sum the digits of an integer with a while loop (sign ignored): -472 -> 13.

    Hint: n % 10 is the last digit; n // 10 drops it.
    """
    raise NotImplementedError('TODO: implement digit_sum')


def collatz_steps(n: int) -> int:
    """Steps to reach 1: halve even n, otherwise n = 3n + 1. Raise ValueError if n < 1."""
    raise NotImplementedError('TODO: implement collatz_steps')


def primes_up_to(limit: int) -> list[int]:
    """All primes <= limit, using nested loops (no imports)."""
    raise NotImplementedError('TODO: implement primes_up_to')


def number_pyramid(rows: int) -> list[str]:
    """Rows of increasing numbers: number_pyramid(3) -> ['1', '1 2', '1 2 3']."""
    raise NotImplementedError('TODO: implement number_pyramid')
