"""Intermediate practice 2 — Iterators, generators, closures, decorators, itertools.

Companion to intermediate/exercises/02_iteration_and_abstractions_exercises.ipynb
and lessons 05–09.
"""
import functools
import itertools
from collections.abc import Callable, Iterable, Iterator


class Countdown:
    """Iterator yielding n, n-1, ..., 0. It is its own iterator (single pass).

    Hint: __iter__ returns self; __next__ raises StopIteration when done.
    """

    def __init__(self, n: int):
        self.current = n

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self.current < 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value


class Squares:
    """Reusable iterable of squares 0..n-1: every `for` loop starts fresh.

    Hint: make __iter__ a generator method instead of returning self.
    """

    def __init__(self, n: int):
        self.n = n

    def __iter__(self) -> Iterator[int]:
        for i in range(self.n):
            yield i * i


def fibonacci(n: int) -> Iterator[int]:
    """Yield the first n Fibonacci numbers: 0, 1, 1, 2, 3, 5, ..."""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


def positive_ints(lines: Iterable[str]) -> Iterator[int]:
    """Lazily yield positive integers from text lines, skipping anything invalid."""
    for line in lines:
        try:
            value = int(line.strip())
        except ValueError:
            continue
        if value > 0:
            yield value


def flatten_one_level(groups: Iterable[Iterable]) -> Iterator:
    """Yield every item of every group. Hint: yield from."""
    for group in groups:
        yield from group


def take(iterable: Iterable, n: int) -> list:
    """Return the first n items, even from an infinite iterator. Hint: itertools.islice."""
    return list(itertools.islice(iterable, n))


def make_tax_adder(rate: float) -> Callable[[float], float]:
    """Return a function that adds `rate` tax to a price (rounded to 2 decimals)."""
    def add_tax(price: float) -> float:
        return round(price * (1 + rate), 2)
    return add_tax


def make_counter() -> Callable[[], int]:
    """Return a function that returns 1, 2, 3, ... on successive calls. Hint: nonlocal."""
    count = 0

    def counter() -> int:
        nonlocal count
        count += 1
        return count
    return counter


def trace(func):
    """Decorator: print 'calling <name>' before each call and return the result unchanged.

    The wrapper must keep the original __name__ and __doc__ (functools.wraps).
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


def require_minimum(minimum: float):
    """Decorator factory: raise ValueError if the first argument is below `minimum`."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(value, *args, **kwargs):
            if value < minimum:
                raise ValueError(f"{func.__name__} needs a value >= {minimum}")
            return func(value, *args, **kwargs)
        return wrapper
    return decorator


class EventRecorder:
    """Context manager that appends 'start' on enter and 'end' on exit to self.events.

    'end' must be recorded even if the block raises, and the error must NOT be swallowed.
    """

    def __init__(self):
        self.events: list[str] = []

    def __enter__(self):
        self.events.append("start")
        return self

    def __exit__(self, exc_type, exc, tb):
        self.events.append("end")
        return False


def sort_employees(rows: list[dict]) -> list[dict]:
    """Sort by 'team' ascending, then 'salary' descending. Hint: key=lambda r: (..., -...)."""
    return sorted(rows, key=lambda row: (row["team"], -row["salary"]))


def power(base: float, exponent: float) -> float:
    """Return base raised to exponent."""
    return base ** exponent


def make_square() -> Callable[[float], float]:
    """Return a one-argument square function built from power() with functools.partial."""
    return functools.partial(power, exponent=2)


@functools.lru_cache(maxsize=None)
def cached_fib(n: int) -> int:
    """Recursive Fibonacci memoized with functools.lru_cache (cached_fib(0) == 0)."""
    return n if n < 2 else cached_fib(n - 1) + cached_fib(n - 2)


def all_variants(colors: list[str], sizes: list[str]) -> list[tuple[str, str]]:
    """Every (color, size) pair, colors in the outer loop. Hint: itertools.product."""
    return list(itertools.product(colors, sizes))


def totals_by_category(rows: list[dict]) -> dict[str, float]:
    """Sum row['amount'] per row['category'] using itertools.groupby (input may be unsorted!)."""
    key = lambda row: row["category"]  # noqa: E731
    return {category: sum(r["amount"] for r in group)
            for category, group in itertools.groupby(sorted(rows, key=key), key=key)}


def non_blank(lines: Iterable[str]) -> Iterator[str]:
    """Lazily yield lines with surrounding whitespace removed, skipping blank ones."""
    return (line.strip() for line in lines if line.strip())
