# Auto-graded practice. Replace each `raise NotImplementedError` with your code.
# Check your work:  python -m pytest practice -k advanced_01_internals_typing_architecture
# Stuck? Re-read the docstring hint, then the lesson notebook it names.
# Reset to a blank copy:  git checkout -- practice/exercises/advanced_01_internals_typing_architecture.py

"""Advanced practice 1 — Data model, descriptors, generics, plugins, dependency injection.

Companion to advanced/exercises/01_internals_typing_architecture_exercises.ipynb and
lessons 00–04 and 12.
"""
from __future__ import annotations
import inspect
from collections.abc import Callable, Iterable, Iterator, Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Generic, Optional, Protocol, TypeVar
T = TypeVar('T')


class ReadOnlyBag:
    """A read-only collection supporting len(), iteration, `in` and a safe repr.

    It copies its input so later changes to the caller's list do not leak in.
    repr shows at most 3 items: ReadOnlyBag([1, 2, 3, ...]) for longer bags.
    """

    def __init__(self, items: Iterable):
        raise NotImplementedError('TODO: implement __init__')

    def __len__(self) -> int:
        raise NotImplementedError('TODO: implement __len__')

    def __iter__(self) -> Iterator:
        raise NotImplementedError('TODO: implement __iter__')

    def __contains__(self, item) -> bool:
        raise NotImplementedError('TODO: implement __contains__')

    def __repr__(self) -> str:
        raise NotImplementedError('TODO: implement __repr__')


class Ticket:
    """Ordered by priority (lower first), then by sequence number.

    __eq__ and __lt__ return NotImplemented for non-Ticket operands, and
    Tickets are hashable on (priority, sequence).
    """

    def __init__(self, priority: int, sequence: int, title: str=''):
        raise NotImplementedError('TODO: implement __init__')

    def _key(self) -> tuple[int, int]:
        raise NotImplementedError('TODO: implement _key')

    def __eq__(self, other):
        raise NotImplementedError('TODO: implement __eq__')

    def __lt__(self, other):
        raise NotImplementedError('TODO: implement __lt__')

    def __hash__(self) -> int:
        raise NotImplementedError('TODO: implement __hash__')


class PositiveInt:
    """Descriptor that only accepts positive ints (TypeError / ValueError otherwise).

    Usage:  class Order:  quantity = PositiveInt()
    Hint: __set_name__ learns the attribute name; store values in instance.__dict__.
    """

    def __set_name__(self, owner, name: str) -> None:
        raise NotImplementedError('TODO: implement __set_name__')

    def __get__(self, instance, owner=None):
        raise NotImplementedError('TODO: implement __get__')

    def __set__(self, instance, value) -> None:
        raise NotImplementedError('TODO: implement __set__')


class Stack(Generic[T]):
    """A typed LIFO stack. pop() on an empty stack raises IndexError('pop from empty stack')."""

    def __init__(self) -> None:
        raise NotImplementedError('TODO: implement __init__')

    def push(self, item: T) -> None:
        raise NotImplementedError('TODO: implement push')

    def pop(self) -> T:
        raise NotImplementedError('TODO: implement pop')

    def __len__(self) -> int:
        raise NotImplementedError('TODO: implement __len__')


def first_or_none(values: Sequence[T]) -> Optional[T]:
    """Return the first element or None, preserving the element type for type checkers."""
    raise NotImplementedError('TODO: implement first_or_none')


class PluginRegistry:
    """Run plugins only by approved name.

    register(name, func) raises ValueError for names not in the allowlist;
    run(name, *args) raises KeyError for unregistered names.
    """

    def __init__(self, allowed: Iterable[str]):
        raise NotImplementedError('TODO: implement __init__')

    def register(self, name: str, func: Callable) -> None:
        raise NotImplementedError('TODO: implement register')

    def run(self, name: str, *args):
        raise NotImplementedError('TODO: implement run')

    def names(self) -> list[str]:
        raise NotImplementedError('TODO: implement names')


def parameter_defaults(func: Callable) -> dict[str, object]:
    """Map each parameter name to its default value, or None if it has no default.

    Hint: inspect.signature(func).parameters and inspect.Parameter.empty.
    """
    raise NotImplementedError('TODO: implement parameter_defaults')


class UserRepository(Protocol):
    """Storage port: anything with get(user_id) and save(user) qualifies."""

    def get(self, user_id: str) -> Optional[dict]:
        raise NotImplementedError('TODO: implement get')

    def save(self, user: dict) -> None:
        raise NotImplementedError('TODO: implement save')


class InMemoryUserRepository:
    """Satisfies UserRepository structurally (no inheritance needed)."""

    def __init__(self) -> None:
        raise NotImplementedError('TODO: implement __init__')

    def get(self, user_id: str) -> Optional[dict]:
        raise NotImplementedError('TODO: implement get')

    def save(self, user: dict) -> None:
        raise NotImplementedError('TODO: implement save')


def rename_user(repo: UserRepository, user_id: str, new_name: str) -> dict:
    """Domain service: validate, load, change, save. Raise KeyError if missing,
    ValueError if new_name is blank. Works with any UserRepository."""
    raise NotImplementedError('TODO: implement rename_user')


@dataclass
class Session:
    """A login session. is_expired() uses an injected clock so tests control time."""
    created_at: datetime
    ttl: timedelta
    clock: Callable[[], datetime] = datetime.now

    def is_expired(self) -> bool:
        raise NotImplementedError('TODO: implement is_expired')


class Vector:
    """2-D vector supporting +, -, * (by a number, either side), abs(), ==, and hashing.

    repr is 'Vector(x, y)'. Unsupported operands return NotImplemented.
    """
    __slots__ = ('x', 'y')

    def __init__(self, x: float, y: float):
        raise NotImplementedError('TODO: implement __init__')

    def __add__(self, other):
        raise NotImplementedError('TODO: implement __add__')

    def __sub__(self, other):
        raise NotImplementedError('TODO: implement __sub__')

    def __mul__(self, factor):
        raise NotImplementedError('TODO: implement __mul__')
    __rmul__ = __mul__

    def __abs__(self) -> float:
        raise NotImplementedError('TODO: implement __abs__')

    def __eq__(self, other):
        raise NotImplementedError('TODO: implement __eq__')

    def __hash__(self) -> int:
        raise NotImplementedError('TODO: implement __hash__')

    def __repr__(self) -> str:
        raise NotImplementedError('TODO: implement __repr__')


class LRUCache:
    """Fixed-capacity cache: get() marks a key as recently used; put() evicts the least
    recently used key when full. get() of a missing key returns None. Hint: OrderedDict."""

    def __init__(self, capacity: int):
        raise NotImplementedError('TODO: implement __init__')

    def get(self, key):
        raise NotImplementedError('TODO: implement get')

    def put(self, key, value) -> None:
        raise NotImplementedError('TODO: implement put')

    def keys(self) -> list:
        """Keys from least to most recently used."""
        raise NotImplementedError('TODO: implement keys')


class Plugin:
    """Base class whose subclasses register themselves by `name` via __init_subclass__.

    Plugin.registry maps name -> subclass. A subclass without a `name` class attribute,
    or with a duplicate name, raises TypeError at class-creation time.
    """
    registry: dict[str, type] = {}

    def __init_subclass__(cls, **kwargs):
        raise NotImplementedError('TODO: implement __init_subclass__')


def enforce_types(func):
    """Decorator: raise TypeError when an argument is not an instance of its annotation.

    Only check parameters annotated with a plain class (int, str, ...); skip others.
    Hint: inspect.signature(func).bind(*args, **kwargs).
    """
    raise NotImplementedError('TODO: implement enforce_types')
