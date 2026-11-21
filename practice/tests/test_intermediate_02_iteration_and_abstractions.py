import functools
import itertools

import pytest

from grader import check
from practice_loader import module_for

m = module_for(__file__)


def test_countdown_is_single_pass_iterator():
    countdown = m.Countdown(3)
    assert iter(countdown) is countdown
    check(list(countdown))
    assert list(countdown) == [], "an iterator is exhausted after one pass"
    with pytest.raises(StopIteration):
        next(countdown)


def test_squares_is_reusable():
    squares = m.Squares(4)
    first = list(squares)
    check(first)
    assert list(squares) == first, "an iterable should give a fresh iterator each time"


def test_fibonacci_is_lazy():
    gen = m.fibonacci(10)
    assert iter(gen) is gen, "fibonacci() should be a generator (use yield)"
    check(list(gen))
    assert list(m.fibonacci(0)) == []


def test_positive_ints():
    check(list(m.positive_ints(["5", " 12 ", "-3", "0", "abc", "", "7"])))


def test_positive_ints_is_lazy():
    def lines():
        yield "1"
        raise AssertionError("read too far: process lines one at a time")
    next(iter(m.positive_ints(lines())))


def test_flatten_one_level():
    check(list(m.flatten_one_level([[1, 2], (3,), [], [[4]]])))


def test_take_from_infinite():
    check(m.take(itertools.count(10), 3))
    check(m.take([1, 2], 5))


def test_make_tax_adder():
    add_vat, add_low = m.make_tax_adder(0.2), m.make_tax_adder(0.05)
    check(add_vat(10))
    check(add_low(10), hint="each closure remembers its own rate")


def test_make_counter():
    first, second = m.make_counter(), m.make_counter()
    check([first(), first(), first()])
    check(second(), hint="counters must be independent")


def test_trace(capsys):
    @m.trace
    def add(a, b):
        """Add two numbers."""
        return a + b

    assert add(2, 3) == 5
    check(capsys.readouterr().out.strip())
    assert add.__name__ == "add" and add.__doc__ == "Add two numbers.", "use functools.wraps"


def test_require_minimum():
    @m.require_minimum(18)
    def register(age, name="x"):
        return f"{name}:{age}"

    assert register(18, name="Ana") == "Ana:18"
    with pytest.raises(ValueError):
        register(17)
    assert register.__name__ == "register"


def test_event_recorder():
    recorder = m.EventRecorder()
    with recorder as entered:
        assert entered is recorder
        check(list(recorder.events))
    check(recorder.events)


def test_event_recorder_does_not_swallow_errors():
    recorder = m.EventRecorder()
    with pytest.raises(KeyError):
        with recorder:
            raise KeyError("boom")
    check(recorder.events)


def test_sort_employees():
    rows = [{"name": "a", "team": "ops", "salary": 50}, {"name": "b", "team": "dev", "salary": 70},
            {"name": "c", "team": "dev", "salary": 90}, {"name": "d", "team": "ops", "salary": 60}]
    check([r["name"] for r in m.sort_employees(rows)])


def test_make_square_uses_partial():
    square = m.make_square()
    assert isinstance(square, functools.partial)
    check(square(7))
    check(m.power(2, 10))


def test_cached_fib():
    m.cached_fib.cache_clear()
    check(m.cached_fib(80))
    assert m.cached_fib.cache_info().hits > 0, "decorate with functools.lru_cache"


def test_all_variants():
    check(m.all_variants(["red", "blue"], ["S", "M"]))


def test_totals_by_category_with_unsorted_input():
    rows = [{"category": "b", "amount": 1}, {"category": "a", "amount": 2}, {"category": "b", "amount": 3}]
    check(m.totals_by_category(rows), hint="groupby only groups ADJACENT items")
    adjustments = [
        {"category": "paper", "amount": 7},
        {"category": "pens", "amount": 0},
        {"category": "paper", "amount": -2},
        {"category": "pens", "amount": 3},
    ]
    original = [dict(row) for row in adjustments]
    assert m.totals_by_category(adjustments) == {"paper": 5, "pens": 3}, (
        "Combine non-adjacent entries, including refunds and zero amounts"
    )
    assert adjustments == original, "Do not change the caller's records"
    assert m.totals_by_category([]) == {}, "No records means no totals"


def test_non_blank():
    check(list(m.non_blank(["  a ", "", "   ", "b\n"])))


def test_chunked():
    check(list(m.chunked(range(7), 3)))
    def guarded_stream():
        yield from range(1000)
        raise AssertionError("Requesting two batches should not exhaust a long input.")

    check(list(itertools.islice(m.chunked(guarded_stream(), 2), 2)), hint="must work on streaming input")

    assert list(m.chunked(iter(()), 3)) == []
    stream = iter(["paid", "packed", "shipped"])
    batches = iter(m.chunked(stream, 2))
    assert next(batches) == ["paid", "packed"]
    assert list(batches) == [["shipped"]], "Keep the partial dispatch batch."


def test_running_total():
    check(list(m.running_total([3, 1, 4, 1, 5])))
    check(list(m.running_total([])))


@pytest.mark.parametrize("n", [1, 2, 3, 5])
def test_sliding_window(n):
    check(m.sliding_window([1, 2, 3, 4], n))


def test_once():
    calls = []

    @m.once
    def setup(value):
        calls.append(value)
        return value * 10

    check([setup(1), setup(2), setup(3)])
    assert calls == [1], "the wrapped function must run only once"

    calls = []
    @m.once
    def empty(*, key):
        calls.append(key)
        return None
    assert empty(key="first") is None and empty(key="later") is None
    assert calls == ["first"], "A successful None result must be remembered."


def test_count_calls():
    @m.count_calls
    def ping():
        return "pong"

    assert ping.calls == 0
    ping()
    ping()
    check(ping.calls)
    assert ping.__name__ == "ping"
