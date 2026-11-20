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
    conn.executescript(
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
        cursor = conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    return cursor.lastrowid


def list_tasks(conn: sqlite3.Connection, done=None) -> list[tuple[int, str, bool]]:
    """Return (id, title, done) tuples ordered by id; filter by done when it is not None."""
    sql, params = "SELECT id, title, done FROM tasks", ()
    if done is not None:
        sql, params = sql + " WHERE done = ?", (int(done),)
    return [(i, t, bool(d)) for i, t, d in conn.execute(sql + " ORDER BY id", params)]


def complete_task(conn: sqlite3.Connection, task_id: int) -> bool:
    """Mark a task done. Return False if no task has that id."""
    with conn:
        return conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,)).rowcount == 1


def delete_task(conn: sqlite3.Connection, task_id: int) -> bool:
    """Delete a task. Return False if no task has that id."""
    with conn:
        return conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,)).rowcount == 1


def transfer(conn: sqlite3.Connection, source: str, target: str, amount: float) -> None:
    """Move money between accounts atomically.

    If the CHECK constraint fails (overdraft) or an account is missing, raise
    ValueError and leave BOTH balances unchanged. Hint: `with conn:` commits or rolls back.
    """
    try:
        with conn:
            for name, delta in ((source, -amount), (target, amount)):
                updated = conn.execute("UPDATE accounts SET balance = balance + ? WHERE name = ?",
                                       (delta, name)).rowcount
                if updated != 1:
                    raise ValueError(f"unknown account: {name}")
    except sqlite3.IntegrityError as error:
        raise ValueError("insufficient funds") from error


def count_by_status(conn: sqlite3.Connection) -> dict[str, int]:
    """Return {'open': n, 'done': m} using one GROUP BY query."""
    counts = {"open": 0, "done": 0}
    for done, total in conn.execute("SELECT done, COUNT(*) FROM tasks GROUP BY done"):
        counts["done" if done else "open"] = total
    return counts


def build_request(url: str) -> urllib.request.Request:
    """Build a GET Request with headers Accept: application/json and User-Agent: course-client/1.0."""
    return urllib.request.Request(url, method="GET", headers={
        "Accept": "application/json", "User-Agent": "course-client/1.0"})


def fetch_json(url: str, opener: Callable = urllib.request.urlopen, timeout: float = 5.0):
    """Fetch and decode JSON. `opener(request, timeout=...)` returns an object with .read().

    Raise ValueError if the body is not valid JSON. The opener is injected so
    tests never touch the network.
    """
    with opener(build_request(url), timeout=timeout) as response:
        body = response.read()
    try:
        return json.loads(body)
    except json.JSONDecodeError as error:
        raise ValueError("response was not valid JSON") from error


def collect_pages(fetch_page: Callable[[str], dict], first: str, max_pages: int = 100) -> list:
    """Follow {'items': [...], 'next': <page or None>} pages and return all items.

    Raise RuntimeError if more than max_pages pages are visited (protects against loops).
    """
    items, page, visited = [], first, 0
    while page is not None:
        visited += 1
        if visited > max_pages:
            raise RuntimeError("too many pages")
        data = fetch_page(page)
        items.extend(data["items"])
        page = data.get("next")
    return items


def build_parser() -> argparse.ArgumentParser:
    """CLI: `tasks add TITLE` and `tasks list [--done]`; a subcommand is required."""
    parser = argparse.ArgumentParser(prog="tasks")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add", help="add a task")
    add.add_argument("title")
    listing = sub.add_parser("list", help="list tasks")
    listing.add_argument("--done", action="store_true", help="only show finished tasks")
    return parser
