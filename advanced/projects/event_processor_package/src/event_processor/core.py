"""Validated events and transactional SQLite idempotency."""

from __future__ import annotations

from dataclasses import dataclass
import sqlite3


@dataclass(frozen=True)
class Event:
    event_id: str
    category: str
    amount: int

    def __post_init__(self) -> None:
        if not isinstance(self.event_id, str) or not self.event_id.strip():
            raise ValueError("event_id must be nonempty text")
        if not isinstance(self.category, str) or not self.category.strip():
            raise ValueError("category must be nonempty text")
        if isinstance(self.amount, bool) or not isinstance(self.amount, int) or self.amount < 0:
            raise ValueError("amount must be a nonnegative integer")


def parse_event(raw: object) -> Event:
    if not isinstance(raw, dict):
        raise ValueError("expected a JSON object")
    try:
        return Event(raw["event_id"], raw["category"], raw["amount"])
    except KeyError as error:
        raise ValueError(f"missing field: {error.args[0]}") from error


def initialize(db: sqlite3.Connection) -> None:
    with db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS processed_events (
                event_id TEXT PRIMARY KEY,
                category TEXT NOT NULL,
                amount INTEGER NOT NULL CHECK(amount >= 0)
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS totals (
                category TEXT PRIMARY KEY,
                total INTEGER NOT NULL CHECK(total >= 0)
            )
        """)


def apply_event(db: sqlite3.Connection, event: Event) -> str:
    """Return accepted or replayed; reject a conflicting event identifier."""
    with db:
        previous = db.execute(
            "SELECT category, amount FROM processed_events WHERE event_id=?",
            (event.event_id,),
        ).fetchone()
        if previous is not None:
            if previous != (event.category, event.amount):
                raise ValueError("idempotency key conflict")
            return "replayed"
        db.execute(
            "INSERT INTO processed_events(event_id, category, amount) VALUES (?, ?, ?)",
            (event.event_id, event.category, event.amount),
        )
        db.execute("""
            INSERT INTO totals(category, total) VALUES (?, ?)
            ON CONFLICT(category) DO UPDATE SET total = total + excluded.total
        """, (event.category, event.amount))
    return "accepted"


def category_totals(db: sqlite3.Connection) -> dict[str, int]:
    return dict(db.execute("SELECT category, total FROM totals ORDER BY category").fetchall())
