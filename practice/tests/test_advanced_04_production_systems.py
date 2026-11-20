import sqlite3
import uuid
from datetime import datetime, timezone

import pytest

from grader import check
from practice_loader import module_for

m = module_for(__file__)


def test_make_event():
    fixed = datetime(2024, 5, 1, 8, 30, tzinfo=timezone.utc)
    check(m.make_event("order.created", "abc", clock=lambda: fixed))
    generated = m.make_event("x")["correlation_id"]
    assert uuid.UUID(generated).version == 4


@pytest.mark.parametrize("samples", [list(range(1, 101)), [7], [30, 10, 20], [5, 1, 9, 3]])
def test_latency_summary(samples):
    check(m.latency_summary(samples), hint="nearest-rank p95")


def test_latency_summary_empty():
    with pytest.raises(ValueError):
        m.latency_summary([])


@pytest.mark.parametrize("successes, total", [(999, 1000), (2, 3), (0, 0)])
def test_availability(successes, total):
    check(m.availability(successes, total))


@pytest.mark.parametrize("target, volume", [(99.9, 1_000_000), (99.0, 250), (100, 10), (99.95, 10_000)])
def test_error_budget(target, volume):
    check(m.error_budget(target, volume), hint="round DOWN")


def test_serialize_user_versions():
    user = {"id": 7, "name": "Ana", "email": "ana@x.io", "password_hash": "..."}
    check(m.serialize_user(user))
    check(m.serialize_user(user, version=2))
    check(m.serialize_user({"id": 1, "name": "B"}, version=2))
    with pytest.raises(ValueError):
        m.serialize_user(user, version=3)


def test_error_envelope():
    check(m.error_envelope("not_found", "No such order", 404))
    check(m.error_envelope("db_down", "psycopg: password auth failed for admin", 503))


def test_iterate_cursor():
    pages = {None: {"items": [1], "cursor": "c2"}, "c2": {"items": [2, 3], "cursor": "c3"},
             "c3": {"items": [], "cursor": None}}
    check(m.iterate_cursor(pages.__getitem__))


def test_iterate_cursor_detects_repeats():
    pages = {None: {"items": [1], "cursor": "a"}, "a": {"items": [2], "cursor": "b"},
             "b": {"items": [3], "cursor": "a"}}
    with pytest.raises(RuntimeError) as caught:
        m.iterate_cursor(pages.__getitem__)
    if isinstance(caught.value, NotImplementedError):  # a subclass of RuntimeError
        raise caught.value


def test_idempotency_store(tmp_path):
    db = tmp_path / "idem.db"
    calls = []

    def action():
        calls.append(1)
        return {"receipt": len(calls)}

    store = m.IdempotencyStore(sqlite3.connect(db))
    first = store.execute("k1", action)
    assert store.execute("k1", action) == first
    # A new process (new connection) must still see the stored result: it is durable.
    assert m.IdempotencyStore(sqlite3.connect(db)).execute("k1", action) == first
    assert len(calls) == 1


def test_idempotency_store_does_not_store_failures():
    store = m.IdempotencyStore(sqlite3.connect(":memory:"))

    def boom():
        raise RuntimeError("payment gateway down")

    with pytest.raises(RuntimeError):
        store.execute("k", boom)
    assert store.execute("k", lambda: "ok") == "ok", "a failed action can be retried"


@pytest.mark.parametrize("rates", [[0.01, 0.2, 0.3, 0.4], [0.2, 0.3, 0.01, 0.4], [0.5, 0.5], []])
def test_should_alert(rates):
    check(m.should_alert(rates, threshold=0.1, sustained=3))


def test_readiness():
    def broken():
        raise ConnectionError("db unreachable")
    check(m.readiness({"db": broken, "cache": lambda: True}))
    check(m.readiness({"cache": lambda: True}))
    check(m.readiness({"disk": lambda: False}))


def test_migrate_is_versioned_and_idempotent():
    conn = sqlite3.connect(":memory:")
    migrations = ["CREATE TABLE users (id INTEGER PRIMARY KEY)",
                  "ALTER TABLE users ADD COLUMN email TEXT"]
    check(m.migrate(conn, migrations[:1]))
    check(m.migrate(conn, migrations))
    check(m.migrate(conn, migrations), hint="re-running must not apply anything twice")
    check([row[1] for row in conn.execute("PRAGMA table_info(users)")])


@pytest.mark.parametrize("text", ["1.2.3", "v10.0.1"])
def test_parse_version(text):
    check(m.parse_version(text))


@pytest.mark.parametrize("bad", ["1.2", "1.2.x", "", "1.2.3.4"])
def test_parse_version_rejects(bad):
    with pytest.raises(ValueError):
        m.parse_version(bad)


@pytest.mark.parametrize("client, server", [("1.2.0", "1.4.9"), ("1.4.0", "1.2.0"), ("1.0.0", "2.0.0"), ("2.1.3", "2.1.0")])
def test_is_compatible(client, server):
    check(m.is_compatible(client, server))
