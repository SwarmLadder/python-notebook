# Auto-graded practice. Replace each `raise NotImplementedError` with your code.
# Check your work:  python -m pytest practice -k basics_04_functions_and_files
# Stuck? Re-read the docstring hint, then the lesson notebook it names.
# Reset to a blank copy:  git checkout -- practice/exercises/basics_04_functions_and_files.py

"""Basics practice 4 — Functions, errors, modules and files.

Companion to basics/exercises/04_functions_and_files_exercises.ipynb and lessons 10–15.
Every file function receives a path, so tests can use a temporary folder.
"""
import csv
import random
from pathlib import Path


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit: F = C * 9/5 + 32."""
    raise NotImplementedError('TODO: implement celsius_to_fahrenheit')


def min_max(values: list[float]) -> tuple[float, float]:
    """Return (minimum, maximum). Raise ValueError for an empty list."""
    raise NotImplementedError('TODO: implement min_max')


def average(values: list[float]) -> float:
    """Return the mean. Raise ValueError with a clear message for an empty list."""
    raise NotImplementedError('TODO: implement average')


def price_with_tax(price: float, tax_rate: float=0.2) -> float:
    """Return price including tax, rounded to 2 decimals. The default rate is 20%."""
    raise NotImplementedError('TODO: implement price_with_tax')


def is_prime(n: int) -> bool:
    """True if n is a prime number. Numbers below 2 are not prime."""
    raise NotImplementedError('TODO: implement is_prime')


def parse_number(text: str):
    """Return float(text), or None if the text is not a valid number (catch ValueError)."""
    raise NotImplementedError('TODO: implement parse_number')


def check_percentage(value: float) -> float:
    """Return value unchanged if 0–100, otherwise raise ValueError."""
    raise NotImplementedError('TODO: implement check_percentage')


def score_report(names: list[str], scores: list[int]) -> list[str]:
    """Pair names with scores using zip and number them with enumerate (starting at 1).

    >>> score_report(["Ana", "Ben"], [90, 72])
    ['1. Ana: 90', '2. Ben: 72']
    """
    raise NotImplementedError('TODO: implement score_report')


def roll_dice(count: int, seed: int) -> list[int]:
    """Return `count` dice rolls (1–6). The same seed must give the same rolls.

    Hint: random.Random(seed) creates a private, reproducible generator.
    """
    raise NotImplementedError('TODO: implement roll_dice')


def write_lines(path: Path, lines: list[str]) -> None:
    """Write each string on its own line in a UTF-8 text file."""
    raise NotImplementedError('TODO: implement write_lines')


def read_lines(path: Path) -> list[str]:
    """Read a UTF-8 text file and return its lines without trailing newlines."""
    raise NotImplementedError('TODO: implement read_lines')


def count_nonblank_lines(path: Path) -> int:
    """Count lines that contain something other than whitespace."""
    raise NotImplementedError('TODO: implement count_nonblank_lines')


def write_students_csv(path: Path, rows: list[dict]) -> None:
    """Write rows with keys 'name' and 'grade' to CSV (with a header) via csv.DictWriter."""
    raise NotImplementedError('TODO: implement write_students_csv')


def read_grades(path: Path) -> dict[str, int]:
    """Read a name,grade CSV with csv.DictReader and return {name: int(grade)}."""
    raise NotImplementedError('TODO: implement read_grades')


def save_tasks(path: Path, tasks: list[str]) -> None:
    """Save tasks, one per line, UTF-8 (tasks may contain accents or emoji)."""
    raise NotImplementedError('TODO: implement save_tasks')


def load_tasks(path: Path) -> list[str]:
    """Load tasks saved by save_tasks. A missing file means no tasks: return []."""
    raise NotImplementedError('TODO: implement load_tasks')


def safe_divide(a: float, b: float):
    """Return a / b, or None when b is zero (catch ZeroDivisionError)."""
    raise NotImplementedError('TODO: implement safe_divide')


def describe(*numbers: float) -> dict[str, float]:
    """Accept any number of arguments; return {'count', 'total', 'mean'} (mean 0 for none)."""
    raise NotImplementedError('TODO: implement describe')


def discount_price(price: float, *, percent: float=10) -> float:
    """Keyword-only percent (callers must write percent=...). Round to 2 decimals.

    Raise ValueError if percent is outside 0–100.
    """
    raise NotImplementedError('TODO: implement discount_price')


def append_log(path: Path, message: str) -> int:
    """Append message as a new line in a UTF-8 file (create it if missing) and return the
    total number of lines now in the file. Hint: open(path, 'a', encoding='utf-8')."""
    raise NotImplementedError('TODO: implement append_log')


def longest_word_in_file(path: Path) -> str:
    """Return the longest word in a text file (first one wins ties); '' for an empty file."""
    raise NotImplementedError('TODO: implement longest_word_in_file')
