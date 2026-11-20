import sqlite3
import uuid
from datetime import datetime, timezone

import pytest

from practice_loader import module_for

m = module_for(__file__)


def test_make_event():
    fixed = datetime(2024, 5, 1, 8, 30, tzinfo=timezone.utc)
    event = m.make_event("order.created", "abc", clock=lambda: fixed)
    assert event == {"version": 1, "code": "order.created", "correlation_id": "abc",
                     "timestamp": "2024-05-01T08:30:00+00:00"}
    generated = m.make_event("x")["correlation_id"]
    assert uuid.UUID(generated).version == 4


def test_latency_summary():
    samples = list(range(1, 101))
    assert m.latency_summary(samples) == {"count": 100, "median": 50.5, "p95": 95}
    assert m.latency_summary([7]) == {"count": 1, "median": 7, "p95": 7}
    assert m.latency_summary([30, 10, 20])["p95"] == 30
    with pytest.raises(ValueError):
        m.latency_summary([])


def test_availability():
    assert m.availability(999, 1000) == 99.9
    assert m.availability(2, 3) == 66.667
    assert m.availability(0, 0) == 100.0


@pytest.mark.parametrize("target, volume, budget", [(99.9, 1_000_000, 1000), (99.0, 250, 2), (100, 10, 0), (99.95, 10_000, 5)])
def test_error_budget(target, volume, budget):
    assert m.error_budget(target, volume) == budget


def test_serialize_user_versions():
    user = {"id": 7, "name": "Ana", "email": "ana@x.io", "password_hash": "..."}
    assert m.serialize_user(user) == {"id": 7, "name": "Ana"}
    assert m.serialize_user(user, version=2) == {"id": 7, "name": "Ana", "email": "ana@x.io"}
    assert m.serialize_user({"id": 1, "name": "B"}, version=2)["email"] is None
    with pytest.raises(ValueError):
        m.serialize_user(user, version=3)


def test_error_envelope():
    assert m.error_envelope("not_found", "No such order", 404) == {
        "error": {"code": "not_found", "message": "No such order", "status": 404}}
    hidden = m.error_envelope("db_down", "psycopg: password auth failed for admin", 503)
    assert hidden["error"]["message"] == "Internal server error"


def test_iterate_cursor():
    pages = {None: {"items": [1], "cursor": "c2"}, "c2": {"items": [2, 3], "cursor": "c3"},
             "c3": {"items": [], "cursor": None}}
    assert m.iterate_cursor(pages.__getitem__) == [1, 2, 3]


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
    assert store.execute("k1", action) == {"receipt": 1}
    assert store.execute("k1", action) == {"receipt": 1}
    # A new process (new connection) must still see the stored result: it is durable.
    assert m.IdempotencyStore(sqlite3.connect(db)).execute("k1", action) == {"receipt": 1}
    assert len(calls) == 1


def test_idempotency_store_does_not_store_failures():
    store = m.IdempotencyStore(sqlite3.connect(":memory:"))

    def boom():
        raise RuntimeError("payment gateway down")

    with pytest.raises(RuntimeError):
        store.execute("k", boom)
    assert store.execute("k", lambda: "ok") == "ok", "a failed action can be retried"
