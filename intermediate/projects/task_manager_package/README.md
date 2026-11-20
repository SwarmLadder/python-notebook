# Intermediate SQLite Task Manager

A companion **installable Python package** for the [task manager project notebook](../03_sqlite_task_manager_cli.ipynb).

## Requirements
Python 3.10+; the application uses only Python's standard library. Installing the package from pyproject.toml requires a build backend such as setuptools.

## Install
Activate your virtual environment and run this from the folder containing pyproject.toml:

    python -m pip install -e .

## Usage
These commands create or modify the SQLite file named by --database; use a safe test path.

    intermediate-tasks --database test_tasks.db add "Read Python notes"
    intermediate-tasks --database test_tasks.db add "Write unit tests"
    intermediate-tasks --database test_tasks.db list
    intermediate-tasks --database test_tasks.db done 1
    intermediate-tasks --database test_tasks.db list --completed
    intermediate-tasks --database test_tasks.db remove 2

## Tests

    python -m unittest discover -s tests -v

Tests use fresh in-memory SQLite databases and do not affect a real file.

## Structure
- pyproject.toml: build metadata and console entry point
- src/task_manager/core.py: data validation, CRUD operations, parameterized SQL
- src/task_manager/cli.py: argparse CLI, clear error handling
- tests/test_core.py: independent unittest cases

## Suggested improvements
Add task priority, due dates, filtering, safe migrations, JSON import/export, and CLI integration tests. Explain trade-offs and add tests with every extension.
