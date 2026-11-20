# Fill in every ___ so the function does what its docstring says.
# Check your work:  python -m pytest practice -k basics_02_control_flow   (or use the workbook notebook)
# Stuck? Fail a check twice to unlock the hints.
# Reset this file:  git checkout -- practice/exercises/basics_02_control_flow.py

"""Basics practice 2 — Control flow (if/elif/else, for, while, break).

Companion to basics/exercises/02_control_flow_exercises.ipynb and lessons 05–06.
"""


def classify_temperature(celsius: float) -> str:
    """Return 'freezing' (<= 0), 'cold' (< 15), 'comfortable' (< 25) or 'hot'.

    Hint: test the most restrictive condition first, then use elif.
    """
    if ___:
        return "freezing"
    if ___:
        return "cold"
    if celsius < 25:
        return "comfortable"
    return "hot"


def divisible_by_3_and_5(number: int) -> bool:
    """True when number is divisible by both 3 and 5."""
    return ___


def greatest_of_three(a: float, b: float, c: float) -> float:
    """Return the largest value using comparisons only (do not call max())."""
    largest = a
    if ___:
        largest = b
    if ___:
        largest = c
    return largest


def letter_grade(score: float) -> str:
    """Return 'A' (>= 90), 'B' (>= 80), 'C' (>= 70), 'D' (>= 60) or 'F'.

    Raise ValueError when score is outside 0–100.
    """
    if ___:
        raise ValueError(f"score out of range: {score}")
    for limit, grade in ((90, "A"), (80, "B"), (70, "C"), (60, "D")):
        if ___:
            return grade
    return "F"


def is_valid_password(password: str, min_length: int = 8) -> bool:
    """True if the password has at least min_length characters AND at least one digit.

    Hint: any(character.isdigit() for character in password)
    """
    return ___


def sum_to(n: int) -> int:
    """Sum the integers 1..n with a for loop over range(). sum_to(0) is 0."""
    total = 0
    for value in ___:
        total += ___
    return total


def factorial(n: int) -> int:
    """Compute n! with a while loop. 0! is 1. Raise ValueError for negative n."""
    if ___:
        raise ValueError("n must be nonnegative")
    result = 1
    while ___:
        result *= n
        n -= 1
    return result


def count_vowels(text: str) -> int:
    """Count a, e, i, o, u in text, ignoring case."""
    return ___


def first_above(values: list[float], limit: float = 100):
    """Return the first value greater than limit, or None if there is none.

    Hint: return (or break) as soon as you find it — no need to check the rest.
    """
    for value in ___:
        if ___:
            return value
    return None


def count_signs(values: list[float]) -> dict[str, int]:
    """Return {'positive': ..., 'negative': ..., 'zero': ...} counts."""
    counts = {"positive": 0, "negative": 0, "zero": 0}
    for value in values:
        if ___:
            counts["positive"] += 1
        elif ___:
            counts["negative"] += 1
        else:
            counts["zero"] += 1
    return counts


def triangle(rows: int) -> str:
    """Return a left-aligned triangle of asterisks, one row per line.

    >>> print(triangle(3))
    *
    **
    ***
    """
    lines = []
    for row in ___:
        line = ""
        for _ in range(row):
            line += "*"
        lines.append(line)
    return ___


def multiples_of_seven(n: int) -> list[int]:
    """Return the first n multiples of 7: [7, 14, 21, ...]."""
    return ___


def fizzbuzz(n: int) -> list[str]:
    """Return FizzBuzz for 1..n as strings: 'Fizz' (3), 'Buzz' (5), 'FizzBuzz' (both), else the number."""
    result = []
    for value in range(1, n + 1):
        if ___:
            result.append("FizzBuzz")
        elif ___:
            result.append("Fizz")
        elif ___:
            result.append("Buzz")
        else:
            result.append(str(value))
    return result


def is_leap_year(year: int) -> bool:
    """Leap years are divisible by 4, except centuries, unless divisible by 400."""
    return ___


def digit_sum(n: int) -> int:
    """Sum the digits of an integer with a while loop (sign ignored): -472 -> 13.

    Hint: n % 10 is the last digit; n // 10 drops it.
    """
    n = abs(n)
    total = 0
    while ___:
        total += ___
        n //= 10
    return total


def collatz_steps(n: int) -> int:
    """Steps to reach 1: halve even n, otherwise n = 3n + 1. Raise ValueError if n < 1."""
    if ___:
        raise ValueError("n must be positive")
    steps = 0
    while ___:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps


def primes_up_to(limit: int) -> list[int]:
    """All primes <= limit, using nested loops (no imports)."""
    primes = []
    for candidate in ___:
        for divisor in range(2, int(candidate ** 0.5) + 1):
            if ___:
                break
        else:
            primes.append(candidate)
    return primes


def number_pyramid(rows: int) -> list[str]:
    """Rows of increasing numbers: number_pyramid(3) -> ['1', '1 2', '1 2 3']."""
    return ___
