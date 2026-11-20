# Auto-graded practice. Replace each `raise NotImplementedError` with your code.
# Check your work:  python -m pytest practice -k intermediate_03_data_quality_and_testing
# Stuck? Re-read the docstring hint, then the lesson notebook it names.
# Reset to a blank copy:  git checkout -- practice/exercises/intermediate_03_data_quality_and_testing.py

"""Intermediate practice 3 — Type hints, validation, errors, regex, JSON/CSV, logging.

Companion to intermediate/exercises/03_data_quality_and_testing_exercises.ipynb and
lessons 10–14. (The tests in practice/tests/ are themselves examples of pytest style.)
"""
import csv
import io
import json
import logging
import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Optional, TypedDict


def mean_or_none(values: list[float]) -> Optional[float]:
    """Return the arithmetic mean, or None for an empty list."""
    raise NotImplementedError('TODO: implement mean_or_none')


class ProductRecord(TypedDict):
    """Shape of one product from the API: sku (str), name (str), price (float)."""
    sku: str
    name: str
    price: float


def apply_transform(records: Iterable[dict], transform: Callable[[dict], dict]) -> list[dict]:
    """Apply `transform` to every record and return the new list."""
    raise NotImplementedError('TODO: implement apply_transform')


@dataclass(frozen=True)
class Settings:
    """Client settings. timeout must be > 0 and retries >= 0 (ValueError otherwise)."""
    timeout: float = 5.0
    retries: int = 3

    def __post_init__(self):
        raise NotImplementedError('TODO: implement __post_init__')


class InvalidQuantity(ValueError):
    """Domain error raised by parse_quantity."""


def parse_quantity(text: str) -> int:
    """Parse a nonnegative integer quantity.

    Raise InvalidQuantity for bad input. When int() fails, chain the original
    error:  raise InvalidQuantity(...) from error   (so __cause__ is set).
    """
    raise NotImplementedError('TODO: implement parse_quantity')


def log_request(logger: logging.Logger, url: str, token: str, status: int) -> None:
    """Log 'GET <url> -> <status>' at INFO level. The token must never appear in logs."""
    raise NotImplementedError('TODO: implement log_request')
ORDER_CODE = re.compile('[A-Z]{2}-\\d{4}')


def is_order_code(text: str) -> bool:
    """True for exactly two uppercase letters, a dash, four digits: 'AB-1234'. Hint: fullmatch."""
    raise NotImplementedError('TODO: implement is_order_code')


def extract_date(text: str) -> Optional[dict[str, int]]:
    """Find the first YYYY-MM-DD date; return {'year': ..., 'month': ..., 'day': ...} or None.

    Hint: named groups (?P<year>\\d{4}) and match.groupdict().
    """
    raise NotImplementedError('TODO: implement extract_date')


def redact_phones(text: str) -> str:
    """Replace every 555-1234 style number (3 digits, dash, 4 digits) with '[PHONE]'."""
    raise NotImplementedError('TODO: implement redact_phones')


def parse_products(json_text: str) -> list[dict]:
    """Parse '{"products": [...]}' and return the list.

    Raise ValueError if the JSON is invalid, the top level is not an object, or
    'products' is missing or not a list.
    """
    raise NotImplementedError('TODO: implement parse_products')


def clean_csv(text: str) -> tuple[list[dict], list[int]]:
    """Read CSV text with columns name,price. Return (valid rows, rejected line numbers).

    Valid rows have price converted to float. Line numbers count the header as line 1.
    """
    raise NotImplementedError('TODO: implement clean_csv')


def slugify(title: str) -> str:
    """URL slug: lowercase, runs of non-alphanumerics become one '-', no leading/trailing '-'.

    'Hello, World!  2024' -> 'hello-world-2024'
    """
    raise NotImplementedError('TODO: implement slugify')


def hashtags(text: str) -> list[str]:
    """Unique hashtags (without '#'), lowercase, in first-seen order. '#Py #py #AI' -> ['py', 'ai']."""
    raise NotImplementedError('TODO: implement hashtags')


def parse_settings(text: str) -> dict[str, str]:
    """Parse 'key = value' lines. Skip blank lines and lines starting with '#'.

    Raise ValueError mentioning the line number (e.g. 'line 3') for a line without '='.
    """
    raise NotImplementedError('TODO: implement parse_settings')


def summarize_sales(rows: list[dict]) -> dict[str, float]:
    """Given rows with 'region' and 'amount' (text), return total per region rounded to 2.
    Skip rows whose amount is not a number."""
    raise NotImplementedError('TODO: implement summarize_sales')
