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
    return sum(values) / len(values) if values else None


class ProductRecord(TypedDict):
    """Shape of one product from the API: sku (str), name (str), price (float)."""
    sku: str
    name: str
    price: float


def apply_transform(records: Iterable[dict], transform: Callable[[dict], dict]) -> list[dict]:
    """Apply `transform` to every record and return the new list."""
    return [transform(record) for record in records]


@dataclass(frozen=True)
class Settings:
    """Client settings. timeout must be > 0 and retries >= 0 (ValueError otherwise)."""
    timeout: float = 5.0
    retries: int = 3

    def __post_init__(self):
        if self.timeout <= 0:
            raise ValueError("timeout must be positive")
        if self.retries < 0:
            raise ValueError("retries cannot be negative")


class InvalidQuantity(ValueError):
    """Domain error raised by parse_quantity."""


def parse_quantity(text: str) -> int:
    """Parse a nonnegative integer quantity.

    Raise InvalidQuantity for bad input. When int() fails, chain the original
    error:  raise InvalidQuantity(...) from error   (so __cause__ is set).
    """
    try:
        value = int(text)
    except ValueError as error:
        raise InvalidQuantity(f"not a whole number: {text!r}") from error
    if value < 0:
        raise InvalidQuantity("quantity cannot be negative")
    return value


def log_request(logger: logging.Logger, url: str, token: str, status: int) -> None:
    """Log 'GET <url> -> <status>' at INFO level. The token must never appear in logs."""
    logger.info("GET %s -> %s", url, status)


ORDER_CODE = re.compile(r"[A-Z]{2}-\d{4}")


def is_order_code(text: str) -> bool:
    """True for exactly two uppercase letters, a dash, four digits: 'AB-1234'. Hint: fullmatch."""
    return ORDER_CODE.fullmatch(text) is not None


def extract_date(text: str) -> Optional[dict[str, int]]:
    """Find the first YYYY-MM-DD date; return {'year': ..., 'month': ..., 'day': ...} or None.

    Hint: named groups (?P<year>\\d{4}) and match.groupdict().
    """
    match = re.search(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})", text)
    return {k: int(v) for k, v in match.groupdict().items()} if match else None


def redact_phones(text: str) -> str:
    """Replace every 555-1234 style number (3 digits, dash, 4 digits) with '[PHONE]'."""
    return re.sub(r"\b\d{3}-\d{4}\b", "[PHONE]", text)


def parse_products(json_text: str) -> list[dict]:
    """Parse '{"products": [...]}' and return the list.

    Raise ValueError if the JSON is invalid, the top level is not an object, or
    'products' is missing or not a list.
    """
    try:
        data = json.loads(json_text)
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid JSON: {error}") from error
    if not isinstance(data, dict) or not isinstance(data.get("products"), list):
        raise ValueError("expected an object with a 'products' list")
    return data["products"]


def clean_csv(text: str) -> tuple[list[dict], list[int]]:
    """Read CSV text with columns name,price. Return (valid rows, rejected line numbers).

    Valid rows have price converted to float. Line numbers count the header as line 1.
    """
    rows, rejected = [], []
    for line_number, row in enumerate(csv.DictReader(io.StringIO(text)), start=2):
        try:
            rows.append({"name": row["name"], "price": float(row["price"])})
        except (TypeError, ValueError):
            rejected.append(line_number)
    return rows, rejected
