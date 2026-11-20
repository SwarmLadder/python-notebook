import functools
import itertools

import pytest

from practice_loader import module_for

m = module_for(__file__)


def test_countdown_is_single_pass_iterator():
    countdown = m.Countdown(3)
    assert iter(countdown) is countdown
    assert list(countdown) == [3, 2, 1, 0]
    assert list(countdown) == [], "an iterator is exhausted after one pass"
    with pytest.raises(StopIteration):
        next(countdown)


def test_squares_is_reusable():
    squares = m.Squares(4)
    assert list(squares) == [0, 1, 4, 9]
    assert list(squares) == [0, 1, 4, 9], "an iterable should give a fresh iterator each time"


def test_fibonacci_is_lazy():
    gen = m.fibonacci(7)
    assert next(gen) == 0, "fibonacci() should be a generator (use yield)"
    assert list(gen) == [1, 1, 2, 3, 5, 8]
    assert list(m.fibonacci(0)) == []


def test_positive_ints():
    assert list(m.positive_ints(["5", " 12 ", "-3", "0", "abc", "", "7"])) == [5, 12, 7]


def test_positive_ints_is_lazy():
    def lines():
        yield "1"
        raise AssertionError("read too far: process lines one at a time")
    assert next(iter(m.positive_ints(lines()))) == 1


def test_flatten_one_level():
    assert list(m.flatten_one_level([[1, 2], (3,), [], [[4]]])) == [1, 2, 3, [4]]


def test_take_from_infinite():
    assert m.take(itertools.count(10), 3) == [10, 11, 12]
    assert m.take([1, 2], 5) == [1, 2]


def test_make_tax_adder():
    add_vat = m.make_tax_adder(0.2)
    add_low = m.make_tax_adder(0.05)
    assert add_vat(10) == 12.0
    assert add_low(10) == 10.5, "each closure remembers its own rate"


def test_make_counter():
    first, second = m.make_counter(), m.make_counter()
    assert [first(), first(), first()] == [1, 2, 3]
    assert second() == 1, "counters must be independent"


def test_trace(capsys):
    @m.trace
    def add(a, b):
        """Add two numbers."""
        return a + b

    assert add(2, 3) == 5
    assert capsys.readouterr().out.strip() == "calling add"
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
        assert recorder.events == ["start"]
    assert recorder.events == ["start", "end"]


def test_event_recorder_does_not_swallow_errors():
    recorder = m.EventRecorder()
    with pytest.raises(KeyError):
        with recorder:
            raise KeyError("boom")
    assert recorder.events == ["start", "end"]


def test_sort_employees():
    rows = [{"name": "a", "team": "ops", "salary": 50}, {"name": "b", "team": "dev", "salary": 70},
            {"name": "c", "team": "dev", "salary": 90}, {"name": "d", "team": "ops", "salary": 60}]
    assert [r["name"] for r in m.sort_employees(rows)] == ["c", "b", "d", "a"]


def test_make_square_uses_partial():
    square = m.make_square()
    assert isinstance(square, functools.partial)
    assert square(7) == 49
    assert m.power(2, 10) == 1024


def test_cached_fib():
    m.cached_fib.cache_clear()
    assert m.cached_fib(80) == 23416728348467685
    assert m.cached_fib.cache_info().hits > 0, "decorate with functools.lru_cache"


def test_all_variants():
    assert m.all_variants(["red", "blue"], ["S", "M"]) == [("red", "S"), ("red", "M"), ("blue", "S"), ("blue", "M")]


def test_totals_by_category_with_unsorted_input():
    rows = [{"category": "b", "amount": 1}, {"category": "a", "amount": 2}, {"category": "b", "amount": 3}]
    assert m.totals_by_category(rows) == {"a": 2, "b": 4}


def test_non_blank():
    assert list(m.non_blank(["  a ", "", "   ", "b\n"])) == ["a", "b"]
