# Advanced Transactional Event Processor

This is the standalone companion package to the [advanced event-processing project notebook](../03_transactional_event_processor.ipynb).

**Requirements:** Python 3.11+ and setuptools for editable installation. Runtime behavior uses only the Python standard library.

## Install

Activate a virtual environment, then run this command from the directory containing pyproject.toml:

    python -m pip install -e .

## Usage

Choose a disposable SQLite path. The following commands **create or modify** the database file you provide:

    advanced-events --database demo_events.db process '{"event_id":"E1","category":"books","amount":5}'
    advanced-events --database demo_events.db process '{"event_id":"E1","category":"books","amount":5}'
    advanced-events --database demo_events.db totals

The second submission returns "replayed" and does not double-apply the amount. A conflicting amount with the same event_id is rejected.

## Tests

    python -m unittest discover -s tests -v

Tests use in-memory SQLite databases and do not modify a persistent file.

## Architecture

- src/event_processor/core.py — validated immutable Event model; parameterized SQLite; transactional, idempotent processing
- src/event_processor/cli.py — JSON parsing, CLI arguments, safe public status reporting
- tests/test_core.py — duplicate, conflict, invalid input, and aggregate tests
- pyproject.toml — package metadata and command-line entry point

## Limitations and production considerations

This is an educational offline example, not a payment system. It does not include network authentication, distributed queues, tenant isolation, encryption at rest, retention, or horizontal scaling. Do not use it for financial transfers without a production-grade security and architecture review.
