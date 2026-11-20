# Fill in every ___ so the function does what its docstring says.
# Check your work:  python -m pytest practice -k basics_01_fundamentals   (or use the workbook notebook)
# Stuck? Fail a check twice to unlock the hints.
# Reset this file:  git checkout -- practice/exercises/basics_01_fundamentals.py

"""Basics practice 1 — Fundamentals (variables, numbers, strings, booleans).

Companion to basics/exercises/01_fundamentals_exercises.ipynb and lessons 01–04.
"""
import math


def total_cost(price_text: str, units: int = 7) -> float:
    """Convert a price written as text into a float and return the cost of `units` items.

    >>> total_cost("2.50")
    17.5
    Hint: float() converts text; surrounding spaces are fine for float().
    """
    return ___


def circle_measurements(radius: float) -> tuple[float, float]:
    """Return (area, circumference) for a circle. Raise ValueError for a negative radius.

    Hint: use math.pi; area = pi * r**2, circumference = 2 * pi * r.
    """
    if ___:
        raise ValueError("radius must be nonnegative")
    return math.pi * radius ** 2, 2 * math.pi * radius


def split_minutes(total_minutes: int) -> tuple[int, int]:
    """Convert minutes into (whole hours, remaining minutes).

    >>> split_minutes(135)
    (2, 15)
    Hint: floor division // and modulo %, or divmod().
    """
    return ___


def format_price(product: str, price: float) -> str:
    """Return a label like 'Coffee: $3.50' (always two decimal places).

    Hint: f-string format spec  {value:.2f}
    """
    return ___


def ends(text: str) -> tuple[str, str]:
    """Return (first four characters, last three characters) of a nonempty string.

    >>> ends("notebook")
    ('note', 'ook')
    Hint: slicing text[:4] and text[-3:].
    """
    return ___


def normalize(text: str) -> str:
    """Strip surrounding whitespace and casefold, so '  HeLLo ' becomes 'hello'."""
    return ___


def hyphenate(sentence: str) -> str:
    """Split a sentence into words and join them with hyphens.

    >>> hyphenate("learn  python   today")
    'learn-python-today'
    Hint: split() with no argument also collapses repeated spaces.
    """
    return ___


def is_csv(filename: str) -> bool:
    """True if the filename ends in .csv, ignoring case ('DATA.CSV' counts)."""
    return ___


def is_valid_score(score: float) -> bool:
    """True if 0 <= score <= 100 (both ends included). Hint: chained comparison."""
    return ___


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius, rounded to one decimal place. 72.5 -> 22.5"""
    return ___


def parse_order(order: str) -> tuple[dict[str, int], float]:
    """Parse 'item:quantity:unit_price' entries separated by commas.

    Return (quantities by item, total price rounded to 2 decimals).

    >>> parse_order("apple:2:0.50, bread:1:2.25")
    ({'apple': 2, 'bread': 1}, 3.25)
    Hint: split on ',', then strip() each entry and split on ':'.
    """
    quantities: dict[str, int] = {}
    total = 0.0
    for entry in order.split(","):
        name, quantity_text, price_text = entry.strip().split(":")
        quantity = int(quantity_text)
        quantities[name] = quantities.get(name, 0) + quantity
        total += ___
    return ___


def initials(full_name: str) -> str:
    """Return uppercase initials: 'ada  lovelace' -> 'AL'. Blank input gives ''."""
    return ___


def clock_time(seconds: int) -> str:
    """Format seconds as HH:MM:SS with leading zeros: 3725 -> '01:02:05'."""
    hours, rest = divmod(seconds, 3600)
    minutes, secs = divmod(rest, 60)
    return ___


def is_palindrome(text: str) -> bool:
    """True if text reads the same backwards, ignoring case, spaces and punctuation.

    Hint: keep only characters where ch.isalnum(), then compare with [::-1].
    """
    cleaned = [ch.casefold() for ch in text if ch.isalnum()]
    return ___


def percent_change(old: float, new: float) -> float:
    """Percentage change from old to new, rounded to 1 decimal. Raise ValueError if old is 0."""
    if ___:
        raise ValueError("old value cannot be zero")
    return round((new - old) / old * 100, 1)


def mask_card(number: str) -> str:
    """Hide all but the last 4 digits: '1234 5678 9012 3456' -> '************3456'.

    Ignore spaces. Hint: str.replace and string repetition with *.
    """
    digits = number.replace(" ", "")
    return ___
