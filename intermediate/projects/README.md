# Intermediate Python Portfolio Projects

Three guided, executable notebooks and one installable companion package demonstrate the jump from exercises to real applications.

| Project | Main skills | Notebook |
|---|---|---|
| Library Lending System | OOP, composition, dataclasses, JSON, unittest | [Open](01_library_lending_system.ipynb) |
| Offline API and ETL Pipeline | HTTP transport injection, pagination, JSON validation, CSV export, unittest | [Open](02_offline_api_etl_pipeline.ipynb) |
| SQLite Task Manager | SQLite, SQL constraints, transactions, argparse, packaging, tests | [Open](03_sqlite_task_manager_cli.ipynb) |

## Suggested project submission format

- A short README: problem, audience, setup, expected inputs and outputs.
- Documented domain model and decision-making (not just code screenshots).
- Tests for happy paths, invalid values, and boundary conditions.
- No live network requests during unit tests.
- A note about what would need to change for production use.

## Bonus — Real Python Package

The [task_manager_package](task_manager_package/README.md) folder includes:

- A `pyproject.toml` using setuptools as a build backend
- `src/task_manager/core.py` with parameterized SQLite operations
- `src/task_manager/cli.py` exposing an argparse CLI
- `tests/test_core.py` with executable unittest cases

This is the most useful starting point if you want to show an actual Python repository project on GitHub rather than only notebooks.
