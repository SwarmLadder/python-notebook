import os
import random
import re
import sqlite3

import pytest

from grader import check
from practice_loader import module_for

m = module_for(__file__)


def test_parse_limited_json():
    check(m.parse_limited_json('{"a": 1}'))
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


@pytest.mark.parametrize("a, b", [("abc123", "abc123"), ("abc123", "abc124"), ("abc", "abcd")])
def test_tokens_match(a, b):
    check(m.tokens_match(a, b))


def test_grep_command():
    check(m.grep_command("-rf; rm -rf /", "notes.txt"))


def test_redact():
    record = {"user": "ana", "Password": "hunter2", "meta": {"api_key": "k", "ip": "1.2.3.4"}}
    check(m.redact(record))
    assert record["Password"] == "hunter2", "return a copy; do not modify the input"

    nested = {"profile": {"Authorization": {"value": "secret"}}}
    assert m.redact(nested) == {"profile": {"Authorization": "***"}}
    assert nested["profile"]["Authorization"] == {"value": "secret"}, "Keep nested input intact."


def test_limit_text():
    assert m.limit_text("ok", max_chars=2) == "ok"
    with pytest.raises(ValueError):
        m.limit_text("abc", max_chars=2)


def test_stable_priority_queue():
    queue = m.StablePriorityQueue()
    for priority, item in [(2, "c"), (1, "a"), (2, "d"), (1, "b"), (0, {"unorderable": True})]:
        queue.push(priority, item)
    assert len(queue) == 5
    check([queue.pop() for _ in range(5)])
    with pytest.raises(IndexError):
        queue.pop()


@pytest.mark.parametrize("target", [1, 7, 13, 0, 8, 99])
def test_find_index(target):
    check(m.find_index([1, 3, 5, 7, 9, 11, 13], target))


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
    before = emails(conn)
    assert before == ["a@x.io", "b@x.io"]
    with pytest.raises(ValueError):
        m.add_users(conn, ["c@x.io", "a@x.io"])
    with pytest.raises(ValueError):
        m.add_users(conn, ["d@x.io", "not-an-email"])
    assert emails(conn) == before, "no partial inserts after a failure"


def test_password_hashing():
    salt = b"fixed-salt-for-test"
    digest = m.hash_password("correct horse", salt, iterations=1000)
    check(digest)
    assert m.verify_password("correct horse", salt, digest, iterations=1000)
    assert not m.verify_password("wrong horse", salt, digest, iterations=1000)
    assert m.hash_password("correct horse", b"other-salt", 1000) != digest, "the salt must matter"


def test_safe_join(tmp_path):
    base = str(tmp_path)
    assert m.safe_join(base, "notes/today.txt") == os.path.join(str(tmp_path.resolve()), "notes", "today.txt")
    for attack in ("../secret.txt", "a/../../etc/passwd", "/etc/passwd"):
        with pytest.raises(ValueError):
            m.safe_join(base, attack)


def test_merge_sorted():
    check(m.merge_sorted([1, 4, 9], [2, 3, 10], [], [5]))

    assert m.merge_sorted() == []
    assert m.merge_sorted([1, 1], [], [1]) == [1, 1, 1], "Preserve duplicates from every source."


@pytest.mark.parametrize("k", [0, 1, 3, 10])
def test_top_k(k):
    check(m.top_k([5, 1, 9, 3, 7, 9], k))
