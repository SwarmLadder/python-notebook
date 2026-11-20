# Fill in every ___ so the function does what its docstring says.
# Check your work:  python -m pytest practice -k intermediate_04_sql_http_cli   (or use the workbook notebook)
# Stuck? Fail a check twice to unlock the hints.
# Reset this file:  git checkout -- practice/exercises/intermediate_04_sql_http_cli.py

"""Intermediate practice 4 — SQLite, HTTP clients, pagination and argparse.

Companion to intermediate/exercises/04_sql_http_cli_performance_exercises.ipynb and
lessons 15–17. Everything is offline: tests pass in-memory databases and fake openers.
"""
import argparse
import json
import sqlite3
import urllib.request
from collections.abc import Callable


def create_schema(conn: sqlite3.Connection) -> None:
    """Create tables:
    tasks(id INTEGER PRIMARY KEY, title TEXT NOT NULL CHECK(trim(title) != ''),
          done INTEGER NOT NULL DEFAULT 0)
    accounts(name TEXT PRIMARY KEY, balance REAL NOT NULL CHECK(balance >= 0))
    """
    ___(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL CHECK (trim(title) != ''),
            done INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS accounts (
            name TEXT PRIMARY KEY,
            balance REAL NOT NULL CHECK (balance >= 0)
        );
        """
    )


def add_task(conn: sqlite3.Connection, title: str) -> int:
    """Insert a task using a ? placeholder (never string formatting) and return its id."""
    with conn:
        cursor = ___
    return cursor.lastrowid


def list_tasks(conn: sqlite3.Connection, done=None) -> list[tuple[int, str, bool]]:
    """Return (id, title, done) tuples ordered by id; filter by done when it is not None."""
    sql, params = "SELECT id, title, done FROM tasks", ()
    if ___:
        sql, params = sql + " WHERE done = ?", (int(done),)
    return ___


def complete_task(conn: sqlite3.Connection, task_id: int) -> bool:
    """Mark a task done. Return False if no task has that id."""
    with conn:
        return ___


def delete_task(conn: sqlite3.Connection, task_id: int) -> bool:
    """Delete a task. Return False if no task has that id."""
    with conn:
        return ___


def transfer(conn: sqlite3.Connection, source: str, target: str, amount: float) -> None:
    """Move money between accounts atomically.

    If the CHECK constraint fails (overdraft) or an account is missing, raise
    ValueError and leave BOTH balances unchanged. Hint: `with conn:` commits or rolls back.
    """
    try:
        with conn:
            for name, delta in ___:
                updated = conn.execute("UPDATE accounts SET balance = balance + ? WHERE name = ?",
                                       (delta, name)).rowcount
                if ___:
                    raise ValueError(f"unknown account: {name}")
    except sqlite3.IntegrityError as error:
        raise ValueError("insufficient funds") from error


def count_by_status(conn: sqlite3.Connection) -> dict[str, int]:
    """Return {'open': n, 'done': m} using one GROUP BY query."""
    counts = ___
    for done, total in ___:
        counts["done" if done else "open"] = total
    return counts


def build_request(url: str) -> urllib.request.Request:
    """Build a GET Request with headers Accept: application/json and User-Agent: course-client/1.0."""
    return ___


def fetch_json(url: str, opener: Callable = urllib.request.urlopen, timeout: float = 5.0):
    """Fetch and decode JSON. `opener(request, timeout=...)` returns an object with .read().

    Raise ValueError if the body is not valid JSON. The opener is injected so
    tests never touch the network.
    """
    with opener(build_request(url), timeout=timeout) as response:
        body = ___
    try:
        return ___
    except json.JSONDecodeError as error:
        raise ValueError("response was not valid JSON") from error


def collect_pages(fetch_page: Callable[[str], dict], first: str, max_pages: int = 100) -> list:
    """Follow {'items': [...], 'next': <page or None>} pages and return all items.

    Raise RuntimeError if more than max_pages pages are visited (protects against loops).
    """
    items, page, visited = ___
    while ___:
        visited += 1
        if ___:
            raise RuntimeError("too many pages")
        data = fetch_page(page)
        items.extend(data["items"])
        page = data.get("next")
    return items


def build_parser() -> argparse.ArgumentParser:
    """CLI: `tasks add TITLE` and `tasks list [--done]`; a subcommand is required."""
    parser = ___
    sub = ___
    add = sub.add_parser("add", help="add a task")
    add.add_argument("title")
    listing = sub.add_parser("list", help="list tasks")
    listing.add_argument("--done", action="store_true", help="only show finished tasks")
    return parser


def search_tasks(conn: sqlite3.Connection, text: str) -> list[str]:
    """Titles containing text (case-insensitive), ordered by id. Use LIKE with a ? parameter."""
    rows = conn.execute("SELECT title FROM tasks WHERE title LIKE ? ORDER BY id", (f"%{text}%",))
    return ___


def set_setting(conn: sqlite3.Connection, key: str, value: str) -> None:
    """Insert or update a row in settings(key TEXT PRIMARY KEY, value TEXT) — an 'upsert'.

    Hint: INSERT ... ON CONFLICT(key) DO UPDATE SET value = excluded.value
    """
    with conn:
        conn.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)")
        conn.execute("INSERT INTO settings (key, value) VALUES (?, ?) "
                     "ON CONFLICT(key) DO UPDATE SET value = excluded.value", ___)


def build_url(base: str, path: str, params: dict | None = None) -> str:
    """Join base and path with exactly one '/', then add an encoded query string.

    build_url('https://api.x/', '/search', {'q': 'a b'}) -> 'https://api.x/search?q=a+b'
    Hint: urllib.parse.urlencode
    """
    import urllib.parse
    url = base.rstrip("/") + "/" + path.lstrip("/")
    return ___


def paginate(items: list, page: int, per_page: int) -> dict:
    """Return {'items': page slice, 'page': page, 'pages': total pages}. Pages start at 1.
    Raise ValueError for page < 1 or per_page < 1. An empty list has 0 pages."""
    if ___:
        raise ValueError("page and per_page must be at least 1")
    start = (page - 1) * per_page
    return ___
