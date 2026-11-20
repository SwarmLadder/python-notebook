import io
import json
import sqlite3

import pytest

from practice_loader import module_for

m = module_for(__file__)


@pytest.fixture
def conn():
    connection = sqlite3.connect(":memory:")
    m.create_schema(connection)
    yield connection
    connection.close()


def test_schema_creates_tables(conn):
    names = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
    assert {"tasks", "accounts"} <= names


def test_crud(conn):
    first = m.add_task(conn, "write tests")
    second = m.add_task(conn, "ship")
    assert m.list_tasks(conn) == [(first, "write tests", False), (second, "ship", False)]
    assert m.complete_task(conn, first) is True
    assert m.list_tasks(conn, done=True) == [(first, "write tests", True)]
    assert m.list_tasks(conn, done=False) == [(second, "ship", False)]
    assert m.delete_task(conn, second) is True
    assert m.delete_task(conn, second) is False
    assert m.complete_task(conn, 999) is False


def test_add_task_is_safe_from_sql_injection(conn):
    evil = "x'); DROP TABLE tasks; --"
    task_id = m.add_task(conn, evil)
    assert m.list_tasks(conn) == [(task_id, evil, False)], "use ? placeholders"


def test_blank_title_rejected(conn):
    with pytest.raises(sqlite3.IntegrityError):
        m.add_task(conn, "   ")


def test_count_by_status(conn):
    assert m.count_by_status(conn) == {"open": 0, "done": 0}
    m.add_task(conn, "a")
    m.complete_task(conn, m.add_task(conn, "b"))
    m.add_task(conn, "c")
    assert m.count_by_status(conn) == {"open": 2, "done": 1}


def balances(conn):
    return dict(conn.execute("SELECT name, balance FROM accounts"))


def test_transfer_success_and_rollback(conn):
    with conn:
        conn.executemany("INSERT INTO accounts VALUES (?, ?)", [("ana", 100), ("ben", 0)])
    m.transfer(conn, "ana", "ben", 40)
    assert balances(conn) == {"ana": 60, "ben": 40}
    with pytest.raises(ValueError):
        m.transfer(conn, "ana", "ben", 500)
    assert balances(conn) == {"ana": 60, "ben": 40}, "a failed transfer must change nothing"
    with pytest.raises(ValueError):
        m.transfer(conn, "ana", "ghost", 10)
    assert balances(conn) == {"ana": 60, "ben": 40}, "partial updates must be rolled back"


def test_build_request():
    request = m.build_request("https://api.example/items")
    assert request.get_method() == "GET"
    assert request.get_header("Accept") == "application/json"
    assert request.get_header("User-agent") == "course-client/1.0"


class FakeResponse(io.BytesIO):
    pass


def test_fetch_json_with_fake_opener():
    seen = {}

    def opener(request, timeout):
        seen["url"], seen["timeout"] = request.full_url, timeout
        return FakeResponse(json.dumps({"ok": True}).encode())

    assert m.fetch_json("https://api.example/x", opener=opener, timeout=2) == {"ok": True}
    assert seen == {"url": "https://api.example/x", "timeout": 2}


def test_fetch_json_rejects_malformed_body():
    with pytest.raises(ValueError):
        m.fetch_json("https://x", opener=lambda request, timeout: FakeResponse(b"<html>"))


def test_collect_pages():
    pages = {"p1": {"items": [1, 2], "next": "p2"}, "p2": {"items": [3], "next": "p3"},
             "p3": {"items": [], "next": None}}
    assert m.collect_pages(pages.__getitem__, "p1") == [1, 2, 3]


def test_collect_pages_stops_on_loops():
    looping = {"a": {"items": [1], "next": "a"}}
    with pytest.raises(RuntimeError) as caught:
        m.collect_pages(looping.__getitem__, "a", max_pages=5)
    if isinstance(caught.value, NotImplementedError):  # a subclass of RuntimeError
        raise caught.value


def test_parser():
    parser = m.build_parser()
    args = parser.parse_args(["add", "buy milk"])
    assert (args.command, args.title) == ("add", "buy milk")
    assert parser.parse_args(["list", "--done"]).done is True
    assert parser.parse_args(["list"]).done is False
    with pytest.raises(SystemExit):
        parser.parse_args([])
