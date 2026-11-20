"""Advanced practice 3 — Safe parsing, secrets, subprocess safety, transactions, algorithms.

Companion to advanced/exercises/03_security_testing_performance_exercises.ipynb and
lessons 10–11, 13–14 and 17.
"""
from __future__ import annotations

import bisect
import heapq
import hmac
import itertools
import json
import re
import secrets
import sqlite3
from collections.abc import Sequence

SENSITIVE_KEYS = {"password", "token", "secret", "api_key", "authorization"}


def parse_limited_json(text: str, max_bytes: int = 10_000) -> dict:
    """Parse a JSON object safely.

    Check the size (UTF-8 bytes) BEFORE parsing; raise ValueError if too big, if
    the JSON is invalid, or if the top level is not an object.
    """
    if len(text.encode("utf-8")) > max_bytes:
        raise ValueError("payload too large")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        raise ValueError("invalid JSON") from error
    if not isinstance(data, dict):
        raise ValueError("expected a JSON object")
    return data


def make_token() -> str:
    """Return a URL-safe random token of at least 32 bytes of entropy (use `secrets`, not `random`)."""
    return secrets.token_urlsafe(32)


def tokens_match(expected: str, provided: str) -> bool:
    """Compare secrets in constant time with hmac.compare_digest."""
    return hmac.compare_digest(expected.encode(), provided.encode())


def grep_command(pattern: str, path: str) -> list[str]:
    """Build an argument list for `grep -n -- PATTERN PATH` (no shell, no string joining).

    The '--' stops a pattern like '-rf' from being read as an option.
    """
    return ["grep", "-n", "--", pattern, path]


def redact(record: dict) -> dict:
    """Return a copy with values of sensitive keys (case-insensitive, nested dicts too) replaced by '***'."""
    cleaned = {}
    for key, value in record.items():
        if key.lower() in SENSITIVE_KEYS:
            cleaned[key] = "***"
        elif isinstance(value, dict):
            cleaned[key] = redact(value)
        else:
            cleaned[key] = value
    return cleaned


def limit_text(text: str, max_chars: int = 1000) -> str:
    """Return text unchanged if short enough; raise ValueError otherwise."""
    if len(text) > max_chars:
        raise ValueError(f"input longer than {max_chars} characters")
    return text


class StablePriorityQueue:
    """Min-priority queue; items with equal priority come out in insertion (FIFO) order.

    Hint: push (priority, sequence_number, item) tuples onto a heapq list.
    """

    def __init__(self) -> None:
        self._heap: list = []
        self._counter = itertools.count()

    def push(self, priority: int, item) -> None:
        heapq.heappush(self._heap, (priority, next(self._counter), item))

    def pop(self):
        if not self._heap:
            raise IndexError("pop from empty queue")
        return heapq.heappop(self._heap)[2]

    def __len__(self) -> int:
        return len(self._heap)


def find_index(sorted_values: Sequence, target) -> int:
    """Binary search with bisect; return the index of target or -1 if absent."""
    index = bisect.bisect_left(sorted_values, target)
    return index if index < len(sorted_values) and sorted_values[index] == target else -1


def add_users(conn: sqlite3.Connection, emails: list[str]) -> None:
    """Insert all emails into users(email UNIQUE) in ONE transaction.

    If any insert fails (duplicate or invalid email), insert none of them and
    raise ValueError. A valid email matches  something@something.something
    """
    pattern = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")
    try:
        with conn:
            for email in emails:
                if not pattern.fullmatch(email):
                    raise ValueError(f"invalid email: {email!r}")
                conn.execute("INSERT INTO users (email) VALUES (?)", (email,))
    except sqlite3.IntegrityError as error:
        raise ValueError("duplicate email") from error
