"""Basics practice 4 — Functions, errors, modules and files.

Companion to basics/exercises/04_functions_and_files_exercises.ipynb and lessons 10–15.
Every file function receives a path, so tests can use a temporary folder.
"""
import csv
import random
from pathlib import Path


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit: F = C * 9/5 + 32."""
    return celsius * 9 / 5 + 32


def min_max(values: list[float]) -> tuple[float, float]:
    """Return (minimum, maximum). Raise ValueError for an empty list."""
    if not values:
        raise ValueError("min_max() needs at least one value")
    return min(values), max(values)


def average(values: list[float]) -> float:
    """Return the mean. Raise ValueError with a clear message for an empty list."""
    if not values:
        raise ValueError("cannot average an empty list")
    return sum(values) / len(values)


def price_with_tax(price: float, tax_rate: float = 0.2) -> float:
    """Return price including tax, rounded to 2 decimals. The default rate is 20%."""
    return round(price * (1 + tax_rate), 2)


def is_prime(n: int) -> bool:
    """True if n is a prime number. Numbers below 2 are not prime."""
    if n < 2:
        return False
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 1
    return True


def parse_number(text: str):
    """Return float(text), or None if the text is not a valid number (catch ValueError)."""
    try:
        return float(text)
    except ValueError:
        return None


def check_percentage(value: float) -> float:
    """Return value unchanged if 0–100, otherwise raise ValueError."""
    if not 0 <= value <= 100:
        raise ValueError(f"percentage must be between 0 and 100, got {value}")
    return value


def score_report(names: list[str], scores: list[int]) -> list[str]:
    """Pair names with scores using zip and number them with enumerate (starting at 1).

    >>> score_report(["Ana", "Ben"], [90, 72])
    ['1. Ana: 90', '2. Ben: 72']
    """
    return [f"{i}. {name}: {score}" for i, (name, score) in enumerate(zip(names, scores), start=1)]


def roll_dice(count: int, seed: int) -> list[int]:
    """Return `count` dice rolls (1–6). The same seed must give the same rolls.

    Hint: random.Random(seed) creates a private, reproducible generator.
    """
    generator = random.Random(seed)
    return [generator.randint(1, 6) for _ in range(count)]


def write_lines(path: Path, lines: list[str]) -> None:
    """Write each string on its own line in a UTF-8 text file."""
    Path(path).write_text("".join(f"{line}\n" for line in lines), encoding="utf-8")


def read_lines(path: Path) -> list[str]:
    """Read a UTF-8 text file and return its lines without trailing newlines."""
    return Path(path).read_text(encoding="utf-8").splitlines()


def count_nonblank_lines(path: Path) -> int:
    """Count lines that contain something other than whitespace."""
    with open(path, encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def write_students_csv(path: Path, rows: list[dict]) -> None:
    """Write rows with keys 'name' and 'grade' to CSV (with a header) via csv.DictWriter."""
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["name", "grade"])
        writer.writeheader()
        writer.writerows(rows)


def read_grades(path: Path) -> dict[str, int]:
    """Read a name,grade CSV with csv.DictReader and return {name: int(grade)}."""
    with open(path, newline="", encoding="utf-8") as handle:
        return {row["name"]: int(row["grade"]) for row in csv.DictReader(handle)}


def save_tasks(path: Path, tasks: list[str]) -> None:
    """Save tasks, one per line, UTF-8 (tasks may contain accents or emoji)."""
    write_lines(path, tasks)


def load_tasks(path: Path) -> list[str]:
    """Load tasks saved by save_tasks. A missing file means no tasks: return []."""
    path = Path(path)
    if not path.exists():
        return []
    return [line for line in read_lines(path) if line]
