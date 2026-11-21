# Fill in every ___ so the function does what its docstring says.
# Check your work:  python -m pytest practice -k basics_04_functions_and_files   (or run check() in the lesson)
# Stuck? Fail a check twice to unlock the hints.
# Reset this file:  git checkout -- practice/exercises/basics_04_functions_and_files.py

"""Basics practice 4 — Functions, errors, modules and files.

Graded by the challenges in lessons 10–15.
Every file function receives a path, so tests can use a temporary folder.
"""
import csv
import random
from pathlib import Path


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit: F = C * 9/5 + 32."""
    return ___


def min_max(values: list[float]) -> tuple[float, float]:
    """Return (minimum, maximum). Raise ValueError for an empty list."""
    if ___:
        raise ValueError("min_max() needs at least one value")
    return min(values), max(values)


def average(values: list[float]) -> float:
    """Return the mean. Raise ValueError with a clear message for an empty list."""
    if ___:
        raise ValueError("cannot average an empty list")
    return sum(values) / len(values)


def price_with_tax(price: float, tax_rate: float = 0.2) -> float:
    """Return price including tax, rounded to 2 decimals. The default rate is 20%."""
    return ___


def is_prime(n: int) -> bool:
    """True if n is a prime number. Numbers below 2 are not prime."""
    if ___:
        return False
    divisor = 2
    while ___:
        if n % divisor == 0:
            return False
        divisor += 1
    return True


def parse_number(text: str):
    """Return float(text), or None if the text is not a valid number (catch ValueError)."""
    ___


def check_percentage(value: float) -> float:
    """Return value unchanged if 0–100, otherwise raise ValueError."""
    if ___:
        raise ValueError(f"percentage must be between 0 and 100, got {value}")
    return value


def score_report(names: list[str], scores: list[int]) -> list[str]:
    """Pair names with scores using zip and number them with enumerate (starting at 1).

    >>> score_report(["Ana", "Ben"], [90, 72])
    ['1. Ana: 90', '2. Ben: 72']
    """
    ___


def roll_dice(count: int, seed: int) -> list[int]:
    """Return `count` dice rolls (1–6). The same seed must give the same rolls.

    Hint: random.Random(seed) creates a private, reproducible generator.
    """
    generator = random.Random(seed)
    return ___


def write_lines(path: Path, lines: list[str]) -> None:
    """Write each string on its own line in a UTF-8 text file."""
    Path(path).write_text(___, encoding="utf-8")


def read_lines(path: Path) -> list[str]:
    """Read a UTF-8 text file and return its lines without trailing newlines."""
    return ___


def count_nonblank_lines(path: Path) -> int:
    """Count lines that contain something other than whitespace."""
    with open(path, encoding="utf-8") as handle:
        return ___


def write_students_csv(path: Path, rows: list[dict]) -> None:
    """Write rows with keys 'name' and 'grade' to CSV (with a header) via csv.DictWriter."""
    with ___ as handle:
        writer = ___
        writer.writeheader()
        writer.writerows(rows)


def read_grades(path: Path) -> dict[str, int]:
    """Read a name,grade CSV with csv.DictReader and return {name: int(grade)}."""
    ___


def save_tasks(path: Path, tasks: list[str]) -> None:
    """Save tasks, one per line, UTF-8 (tasks may contain accents or emoji)."""
    write_lines(___, tasks)


def load_tasks(path: Path) -> list[str]:
    """Load tasks saved by save_tasks. A missing file means no tasks: return []."""
    path = Path(path)
    if ___:
        return ___
    return [line for line in read_lines(path) if line]


def safe_divide(a: float, b: float):
    """Return a / b, or None when b is zero (catch ZeroDivisionError)."""
    try:
        return ___
    except ZeroDivisionError:
        return None


def describe(*numbers: float) -> dict[str, float]:
    """Accept any number of arguments; return {'count', 'total', 'mean'} (mean 0 for none)."""
    total = sum(numbers)
    return ___


def discount_price(price: float, *, percent: float = 10) -> float:
    """Keyword-only percent (callers must write percent=...). Round to 2 decimals.

    Raise ValueError if percent is outside 0–100.
    """
    if ___:
        raise ValueError("percent must be between 0 and 100")
    return round(price * (1 - percent / 100), 2)


def append_log(path: Path, message: str) -> int:
    """Append message as a new line in a UTF-8 file (create it if missing) and return the
    total number of lines now in the file. Hint: open(path, 'a', encoding='utf-8')."""
    ___


def longest_word_in_file(path: Path) -> str:
    """Return the longest word in a text file (first one wins ties); '' for an empty file."""
    longest = ""
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            for word in ___:
                if ___:
                    longest = word
    return longest
