"""Core domain operations and SQLite persistence."""

from __future__ import annotations
import sqlite3


def initialize(connection: sqlite3.Connection) -> None:
    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL CHECK(length(trim(title)) > 0),
            done INTEGER NOT NULL DEFAULT 0 CHECK(done IN (0, 1))
        )
    """)
    connection.commit()


def add_task(connection: sqlite3.Connection, title: str) -> int:
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Task title must not be empty")
    with connection:
        cursor = connection.execute(
            "INSERT INTO tasks (title) VALUES (?)", (title.strip(),)
        )
    return int(cursor.lastrowid)


def list_tasks(
    connection: sqlite3.Connection, completed: bool | None = None
) -> list[tuple[int, str, int]]:
    query = "SELECT id, title, done FROM tasks"
    if completed is None:
        return connection.execute(query + " ORDER BY id").fetchall()
    return connection.execute(
        query + " WHERE done = ? ORDER BY id", (int(completed),)
    ).fetchall()


def complete_task(connection: sqlite3.Connection, task_id: int) -> None:
    with connection:
        cursor = connection.execute(
            "UPDATE tasks SET done = 1 WHERE id = ?", (task_id,)
        )
        if cursor.rowcount == 0:
            raise KeyError(f"No task with id {task_id}")


def remove_task(connection: sqlite3.Connection, task_id: int) -> None:
    with connection:
        cursor = connection.execute(
            "DELETE FROM tasks WHERE id = ?", (task_id,)
        )
        if cursor.rowcount == 0:
            raise KeyError(f"No task with id {task_id}")
