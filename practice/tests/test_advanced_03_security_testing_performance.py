import random
import re
import sqlite3

import pytest

from practice_loader import module_for

m = module_for(__file__)


def test_parse_limited_json():
    assert m.parse_limited_json('{"a": 1}') == {"a": 1}
    for bad in ("[1, 2]", "nope", '"text"'):
        with pytest.raises(ValueError):
            m.parse_limited_json(bad)


def test_parse_limited_json_checks_size_first():
    with pytest.raises(ValueError, match="large"):
        m.parse_limited_json('{"a": "' + "x" * 100 + '"}', max_bytes=50)
    with pytest.raises(ValueError, match="large"):
        m.parse_limited_json("é" * 30, max_bytes=50)  # measure bytes, not characters


def test_make_token():
    tokens = {m.make_token() for _ in range(50)}
    assert len(tokens) == 50
    assert all(re.fullmatch(r"[A-Za-z0-9_-]{43,}", t) for t in tokens)


def test_make_token_ignores_random_seed():
    random.seed(1)
    first = m.make_token()
    random.seed(1)
    assert m.make_token() != first, "use the secrets module, not random"


def test_tokens_match():
    assert m.tokens_match("abc123", "abc123")
    assert not m.tokens_match("abc123", "abc124")
    assert not m.tokens_match("abc", "abcd")


def test_grep_command():
    assert m.grep_command("-rf; rm -rf /", "notes.txt") == ["grep", "-n", "--", "-rf; rm -rf /", "notes.txt"]


def test_redact():
    record = {"user": "ana", "Password": "hunter2", "meta": {"api_key": "k", "ip": "1.2.3.4"}}
    assert m.redact(record) == {"user": "ana", "Password": "***", "meta": {"api_key": "***", "ip": "1.2.3.4"}}
    assert record["Password"] == "hunter2", "return a copy; do not modify the input"


def test_limit_text():
    assert m.limit_text("ok", max_chars=2) == "ok"
    with pytest.raises(ValueError):
        m.limit_text("abc", max_chars=2)


def test_stable_priority_queue():
    queue = m.StablePriorityQueue()
    for priority, item in [(2, "c"), (1, "a"), (2, "d"), (1, "b"), (0, {"unorderable": True})]:
        queue.push(priority, item)
    assert len(queue) == 5
    assert [queue.pop() for _ in range(5)] == [{"unorderable": True}, "a", "b", "c", "d"]
    with pytest.raises(IndexError):
        queue.pop()


@pytest.mark.parametrize("target, index", [(1, 0), (7, 3), (13, 6), (0, -1), (8, -1), (99, -1)])
def test_find_index(target, index):
    assert m.find_index([1, 3, 5, 7, 9, 11, 13], target) == index


def test_find_index_property_against_linear_search():
    rng = random.Random(0)
    for _ in range(100):
        values = sorted(set(rng.sample(range(100), rng.randint(0, 20))))
        target = rng.randint(-5, 105)
        expected = values.index(target) if target in values else -1
        assert m.find_index(values, target) == expected


@pytest.fixture
def conn():
    connection = sqlite3.connect(":memory:")
    connection.execute("CREATE TABLE users (email TEXT UNIQUE NOT NULL)")
    yield connection
    connection.close()


def emails(conn):
    return [row[0] for row in conn.execute("SELECT email FROM users ORDER BY rowid")]


def test_add_users_all_or_nothing(conn):
    m.add_users(conn, ["a@x.io", "b@x.io"])
    assert emails(conn) == ["a@x.io", "b@x.io"]
    with pytest.raises(ValueError):
        m.add_users(conn, ["c@x.io", "a@x.io"])
    with pytest.raises(ValueError):
        m.add_users(conn, ["d@x.io", "not-an-email"])
    assert emails(conn) == ["a@x.io", "b@x.io"], "no partial inserts after a failure"
