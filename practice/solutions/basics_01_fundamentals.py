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
    return float(price_text) * units


def circle_measurements(radius: float) -> tuple[float, float]:
    """Return (area, circumference) for a circle. Raise ValueError for a negative radius.

    Hint: use math.pi; area = pi * r**2, circumference = 2 * pi * r.
    """
    if radius < 0:
        raise ValueError("radius must be nonnegative")
    return math.pi * radius ** 2, 2 * math.pi * radius


def split_minutes(total_minutes: int) -> tuple[int, int]:
    """Convert minutes into (whole hours, remaining minutes).

    >>> split_minutes(135)
    (2, 15)
    Hint: floor division // and modulo %, or divmod().
    """
    return divmod(total_minutes, 60)


def format_price(product: str, price: float) -> str:
    """Return a label like 'Coffee: $3.50' (always two decimal places).

    Hint: f-string format spec  {value:.2f}
    """
    return f"{product}: ${price:.2f}"


def ends(text: str) -> tuple[str, str]:
    """Return (first four characters, last three characters) of a nonempty string.

    >>> ends("notebook")
    ('note', 'ook')
    Hint: slicing text[:4] and text[-3:].
    """
    return text[:4], text[-3:]


def normalize(text: str) -> str:
    """Strip surrounding whitespace and casefold, so '  HeLLo ' becomes 'hello'."""
    return text.strip().casefold()


def hyphenate(sentence: str) -> str:
    """Split a sentence into words and join them with hyphens.

    >>> hyphenate("learn  python   today")
    'learn-python-today'
    Hint: split() with no argument also collapses repeated spaces.
    """
    return "-".join(sentence.split())


def is_csv(filename: str) -> bool:
    """True if the filename ends in .csv, ignoring case ('DATA.CSV' counts)."""
    return filename.lower().endswith(".csv")


def is_valid_score(score: float) -> bool:
    """True if 0 <= score <= 100 (both ends included). Hint: chained comparison."""
    return 0 <= score <= 100


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius, rounded to one decimal place. 72.5 -> 22.5"""
    return round((fahrenheit - 32) * 5 / 9, 1)


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
        total += quantity * float(price_text)
    return quantities, round(total, 2)
