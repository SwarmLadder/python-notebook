# Auto-graded practice. Replace each `raise NotImplementedError` with your code.
# Check your work:  python -m pytest practice -k basics_01_fundamentals
# Stuck? Re-read the docstring hint, then the lesson notebook it names.
# Reset to a blank copy:  git checkout -- practice/exercises/basics_01_fundamentals.py

"""Basics practice 1 — Fundamentals (variables, numbers, strings, booleans).

Companion to basics/exercises/01_fundamentals_exercises.ipynb and lessons 01–04.
"""
import math


def total_cost(price_text: str, units: int=7) -> float:
    """Convert a price written as text into a float and return the cost of `units` items.

    >>> total_cost("2.50")
    17.5
    Hint: float() converts text; surrounding spaces are fine for float().
    """
    raise NotImplementedError('TODO: implement total_cost')


def circle_measurements(radius: float) -> tuple[float, float]:
    """Return (area, circumference) for a circle. Raise ValueError for a negative radius.

    Hint: use math.pi; area = pi * r**2, circumference = 2 * pi * r.
    """
    raise NotImplementedError('TODO: implement circle_measurements')


def split_minutes(total_minutes: int) -> tuple[int, int]:
    """Convert minutes into (whole hours, remaining minutes).

    >>> split_minutes(135)
    (2, 15)
    Hint: floor division // and modulo %, or divmod().
    """
    raise NotImplementedError('TODO: implement split_minutes')


def format_price(product: str, price: float) -> str:
    """Return a label like 'Coffee: $3.50' (always two decimal places).

    Hint: f-string format spec  {value:.2f}
    """
    raise NotImplementedError('TODO: implement format_price')


def ends(text: str) -> tuple[str, str]:
    """Return (first four characters, last three characters) of a nonempty string.

    >>> ends("notebook")
    ('note', 'ook')
    Hint: slicing text[:4] and text[-3:].
    """
    raise NotImplementedError('TODO: implement ends')


def normalize(text: str) -> str:
    """Strip surrounding whitespace and casefold, so '  HeLLo ' becomes 'hello'."""
    raise NotImplementedError('TODO: implement normalize')


def hyphenate(sentence: str) -> str:
    """Split a sentence into words and join them with hyphens.

    >>> hyphenate("learn  python   today")
    'learn-python-today'
    Hint: split() with no argument also collapses repeated spaces.
    """
    raise NotImplementedError('TODO: implement hyphenate')


def is_csv(filename: str) -> bool:
    """True if the filename ends in .csv, ignoring case ('DATA.CSV' counts)."""
    raise NotImplementedError('TODO: implement is_csv')


def is_valid_score(score: float) -> bool:
    """True if 0 <= score <= 100 (both ends included). Hint: chained comparison."""
    raise NotImplementedError('TODO: implement is_valid_score')


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius, rounded to one decimal place. 72.5 -> 22.5"""
    raise NotImplementedError('TODO: implement fahrenheit_to_celsius')


def parse_order(order: str) -> tuple[dict[str, int], float]:
    """Parse 'item:quantity:unit_price' entries separated by commas.

    Return (quantities by item, total price rounded to 2 decimals).

    >>> parse_order("apple:2:0.50, bread:1:2.25")
    ({'apple': 2, 'bread': 1}, 3.25)
    Hint: split on ',', then strip() each entry and split on ':'.
    """
    raise NotImplementedError('TODO: implement parse_order')


def initials(full_name: str) -> str:
    """Return uppercase initials: 'ada  lovelace' -> 'AL'. Blank input gives ''."""
    raise NotImplementedError('TODO: implement initials')


def clock_time(seconds: int) -> str:
    """Format seconds as HH:MM:SS with leading zeros: 3725 -> '01:02:05'."""
    raise NotImplementedError('TODO: implement clock_time')


def is_palindrome(text: str) -> bool:
    """True if text reads the same backwards, ignoring case, spaces and punctuation.

    Hint: keep only characters where ch.isalnum(), then compare with [::-1].
    """
    raise NotImplementedError('TODO: implement is_palindrome')


def percent_change(old: float, new: float) -> float:
    """Percentage change from old to new, rounded to 1 decimal. Raise ValueError if old is 0."""
    raise NotImplementedError('TODO: implement percent_change')


def mask_card(number: str) -> str:
    """Hide all but the last 4 digits: '1234 5678 9012 3456' -> '************3456'.

    Ignore spaces. Hint: str.replace and string repetition with *.
    """
    raise NotImplementedError('TODO: implement mask_card')
