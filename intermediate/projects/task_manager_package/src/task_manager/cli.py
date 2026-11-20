"""CLI entry point for the Intermediate task manager."""

from __future__ import annotations
import argparse
from contextlib import closing
from pathlib import Path
import sqlite3
from .core import add_task, complete_task, initialize, list_tasks, remove_task


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Educational SQLite task manager")
    parser.add_argument("--database", default="tasks.db", help="SQLite file path")
    commands = parser.add_subparsers(dest="command", required=True)
    command_add = commands.add_parser("add", help="Add a task")
    command_add.add_argument("title")
    command_list = commands.add_parser("list", help="List tasks")
    command_list.add_argument("--completed", action="store_true")
    command_done = commands.add_parser("done", help="Mark task completed")
    command_done.add_argument("task_id", type=int)
    command_remove = commands.add_parser("remove", help="Delete task")
    command_remove.add_argument("task_id", type=int)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = make_parser().parse_args(argv)
    try:
        db_path = Path(args.database).expanduser()
        with closing(sqlite3.connect(db_path)) as connection:
            initialize(connection)
            if args.command == "add":
                print(f"Added task {add_task(connection, args.title)}")
            elif args.command == "list":
                completed = True if args.completed else None
                for task_id, title, done in list_tasks(connection, completed):
                    print(f"{task_id:>4} [{'done' if done else 'open'}] {title}")
            elif args.command == "done":
                complete_task(connection, args.task_id)
                print(f"Completed task {args.task_id}")
            elif args.command == "remove":
                remove_task(connection, args.task_id)
                print(f"Removed task {args.task_id}")
    except (ValueError, KeyError, sqlite3.Error, OSError) as error:
        print(f"Error: {error}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
