"""Advanced practice 4 — Observability, SLOs, API contracts, durable idempotency.

Companion to advanced/exercises/04_production_systems_exercises.ipynb and
lessons 15–18.
"""
from __future__ import annotations

import json
import math
import sqlite3
import statistics
import uuid
from collections.abc import Callable
from datetime import datetime, timezone


def make_event(code: str, correlation_id: str | None = None,
               clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc)) -> dict:
    """Return {'version': 1, 'code', 'correlation_id', 'timestamp'} with an ISO-8601 UTC timestamp.

    A missing correlation_id is generated with uuid4. The clock is injectable for tests.
    """
    return {"version": 1, "code": code, "correlation_id": correlation_id or str(uuid.uuid4()),
            "timestamp": clock().isoformat()}


def latency_summary(milliseconds: list[float]) -> dict[str, float]:
    """Return {'count', 'median', 'p95'}; p95 uses the nearest-rank method.

    nearest rank: sort, then take the value at position ceil(0.95 * n) (1-based).
    Raise ValueError for an empty list.
    """
    if not milliseconds:
        raise ValueError("no samples")
    ordered = sorted(milliseconds)
    rank = math.ceil(0.95 * len(ordered))
    return {"count": len(ordered), "median": statistics.median(ordered), "p95": ordered[rank - 1]}


def availability(successes: int, total: int) -> float:
    """Success ratio as a percentage rounded to 3 decimals; 100.0 when total is 0."""
    if total == 0:
        return 100.0
    return round(100 * successes / total, 3)


def error_budget(target_percent: float, requests: int) -> int:
    """How many requests may fail while still meeting the target (round down).

    error_budget(99.9, 1_000_000) == 1000
    """
    return math.floor(requests * (100 - target_percent) / 100 + 1e-9)


def serialize_user(user: dict, version: int = 1) -> dict:
    """v1 -> {'id', 'name'}; v2 adds optional 'email' (None if absent). Other versions: ValueError.

    v1 output must never change: old clients depend on it.
    """
    if version not in (1, 2):
        raise ValueError(f"unsupported version {version}")
    body = {"id": user["id"], "name": user["name"]}
    if version == 2:
        body["email"] = user.get("email")
    return body


def error_envelope(code: str, message: str, status: int) -> dict:
    """Build {'error': {'code', 'message', 'status'}}. For status >= 500 hide internal details:
    message becomes 'Internal server error'."""
    safe_message = "Internal server error" if status >= 500 else message
    return {"error": {"code": code, "message": safe_message, "status": status}}


def iterate_cursor(fetch: Callable[[str | None], dict]) -> list:
    """Follow {'items': [...], 'cursor': next or None} starting from fetch(None).

    Raise RuntimeError if a cursor repeats (the server is looping).
    """
    items, seen, cursor = [], set(), None
    while True:
        page = fetch(cursor)
        items.extend(page["items"])
        cursor = page.get("cursor")
        if cursor is None:
            return items
        if cursor in seen:
            raise RuntimeError(f"cursor repeated: {cursor}")
        seen.add(cursor)


class IdempotencyStore:
    """SQLite-backed idempotency: execute(key, action) runs action() at most once per key
    and stores its JSON-serializable result; later calls return the stored result.

    If action() raises, nothing is stored, so a retry can run it again.
    """

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        with conn:
            conn.execute("CREATE TABLE IF NOT EXISTS idempotency (key TEXT PRIMARY KEY, result TEXT NOT NULL)")

    def execute(self, key: str, action: Callable[[], object]):
        row = self.conn.execute("SELECT result FROM idempotency WHERE key = ?", (key,)).fetchone()
        if row is not None:
            return json.loads(row[0])
        result = action()
        with self.conn:
            self.conn.execute("INSERT INTO idempotency (key, result) VALUES (?, ?)", (key, json.dumps(result)))
        return result
