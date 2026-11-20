"""CLI for processing one JSON event or viewing category totals."""

from __future__ import annotations

import argparse
from contextlib import closing
import json
from pathlib import Path
import sqlite3
from .core import apply_event, category_totals, initialize, parse_event


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(description="Offline transactional event processor")
    cli.add_argument("--database", default="events.db", help="SQLite database path")
    actions = cli.add_subparsers(dest="command", required=True)
    process = actions.add_parser("process", help="Process a JSON event")
    process.add_argument("json_event", help="JSON object containing event_id, category, amount")
    actions.add_parser("totals", help="Display category totals")
    return cli


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        with closing(sqlite3.connect(Path(args.database).expanduser())) as db:
            initialize(db)
            if args.command == "process":
                if len(args.json_event) > 10000:
                    raise ValueError("event JSON exceeds the length limit")
                raw = json.loads(args.json_event)
                event = parse_event(raw)
                status = apply_event(db, event)
                print(json.dumps({"status": status, "event_id": event.event_id}))
            else:
                print(json.dumps(category_totals(db), sort_keys=True))
    except (ValueError, TypeError, sqlite3.Error, json.JSONDecodeError, OSError) as exc:
        print(json.dumps({"status": "error", "code": "INVALID_EVENT_OR_STORAGE"}))
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
