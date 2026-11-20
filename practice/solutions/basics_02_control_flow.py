"""Basics practice 2 — Control flow (if/elif/else, for, while, break).

Companion to basics/exercises/02_control_flow_exercises.ipynb and lessons 05–06.
"""


def classify_temperature(celsius: float) -> str:
    """Return 'freezing' (<= 0), 'cold' (< 15), 'comfortable' (< 25) or 'hot'.

    Hint: test the most restrictive condition first, then use elif.
    """
    if celsius <= 0:
        return "freezing"
    if celsius < 15:
        return "cold"
    if celsius < 25:
        return "comfortable"
    return "hot"


def divisible_by_3_and_5(number: int) -> bool:
    """True when number is divisible by both 3 and 5."""
    return number % 3 == 0 and number % 5 == 0


def greatest_of_three(a: float, b: float, c: float) -> float:
    """Return the largest value using comparisons only (do not call max())."""
    largest = a
    if b > largest:
        largest = b
    if c > largest:
        largest = c
    return largest


def letter_grade(score: float) -> str:
    """Return 'A' (>= 90), 'B' (>= 80), 'C' (>= 70), 'D' (>= 60) or 'F'.

    Raise ValueError when score is outside 0–100.
    """
    if not 0 <= score <= 100:
        raise ValueError(f"score out of range: {score}")
    for limit, grade in ((90, "A"), (80, "B"), (70, "C"), (60, "D")):
        if score >= limit:
            return grade
    return "F"


def is_valid_password(password: str, min_length: int = 8) -> bool:
    """True if the password has at least min_length characters AND at least one digit.

    Hint: any(character.isdigit() for character in password)
    """
    return len(password) >= min_length and any(ch.isdigit() for ch in password)


def sum_to(n: int) -> int:
    """Sum the integers 1..n with a for loop over range(). sum_to(0) is 0."""
    total = 0
    for value in range(1, n + 1):
        total += value
    return total


def factorial(n: int) -> int:
    """Compute n! with a while loop. 0! is 1. Raise ValueError for negative n."""
    if n < 0:
        raise ValueError("n must be nonnegative")
    result = 1
    while n > 1:
        result *= n
        n -= 1
    return result


def count_vowels(text: str) -> int:
    """Count a, e, i, o, u in text, ignoring case."""
    return sum(1 for ch in text.lower() if ch in "aeiou")


def first_above(values: list[float], limit: float = 100):
    """Return the first value greater than limit, or None if there is none.

    Hint: return (or break) as soon as you find it — no need to check the rest.
    """
    for value in values:
        if value > limit:
            return value
    return None


def count_signs(values: list[float]) -> dict[str, int]:
    """Return {'positive': ..., 'negative': ..., 'zero': ...} counts."""
    counts = {"positive": 0, "negative": 0, "zero": 0}
    for value in values:
        if value > 0:
            counts["positive"] += 1
        elif value < 0:
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
    for row in range(1, rows + 1):
        line = ""
        for _ in range(row):
            line += "*"
        lines.append(line)
    return "\n".join(lines)


def multiples_of_seven(n: int) -> list[int]:
    """Return the first n multiples of 7: [7, 14, 21, ...]."""
    return [7 * i for i in range(1, n + 1)]


def fizzbuzz(n: int) -> list[str]:
    """Return FizzBuzz for 1..n as strings: 'Fizz' (3), 'Buzz' (5), 'FizzBuzz' (both), else the number."""
    result = []
    for value in range(1, n + 1):
        if value % 15 == 0:
            result.append("FizzBuzz")
        elif value % 3 == 0:
            result.append("Fizz")
        elif value % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(value))
    return result
