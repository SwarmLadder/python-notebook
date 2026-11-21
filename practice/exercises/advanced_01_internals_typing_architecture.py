# Fill in every ___ so the function does what its docstring says.
# Check your work:  python -m pytest practice -k advanced_01_internals_typing_architecture   (or run check() in the lesson)
# Stuck? Fail a check twice to unlock the hints.
# Reset this file:  git checkout -- practice/exercises/advanced_01_internals_typing_architecture.py

"""Advanced practice 1 — Data model, descriptors, generics, plugins, dependency injection.

Graded by the challenges in lessons 00–04 and 12.
"""
from __future__ import annotations

import inspect
from collections.abc import Callable, Iterable, Iterator, Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Generic, Optional, Protocol, TypeVar

T = TypeVar("T")


class ReadOnlyBag:
    """A read-only collection supporting len(), iteration, `in` and a safe repr.

    It copies its input so later changes to the caller's list do not leak in.
    repr shows at most 3 items: ReadOnlyBag([1, 2, 3, ...]) for longer bags.
    """

    def __init__(self, items: Iterable):
        self._items = ___

    def __len__(self) -> int:
        return ___

    def __iter__(self) -> Iterator:
        return ___

    def __contains__(self, item) -> bool:
        return ___

    def __repr__(self) -> str:
        shown = ", ".join(repr(i) for i in self._items[:3])
        more = ", ..." if len(self._items) > 3 else ""
        return ___


class Ticket:
    """Ordered by priority (lower first), then by sequence number.

    __eq__ and __lt__ return NotImplemented for non-Ticket operands, and
    Tickets are hashable on (priority, sequence).
    """

    def __init__(self, priority: int, sequence: int, title: str = ""):
        self.priority, self.sequence, self.title = ___

    def _key(self) -> tuple[int, int]:
        return ___

    def __eq__(self, other):
        if ___:
            return NotImplemented
        return self._key() == other._key()

    def __lt__(self, other):
        if ___:
            return NotImplemented
        return self._key() < other._key()

    def __hash__(self) -> int:
        return ___


class PositiveInt:
    """Descriptor that only accepts positive ints (TypeError / ValueError otherwise).

    Usage:  class Order:  quantity = PositiveInt()
    Hint: __set_name__ learns the attribute name; store values in instance.__dict__.
    """

    def __set_name__(self, owner, name: str) -> None:
        self.name = ___

    def __get__(self, instance, owner=None):
        if ___:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value) -> None:
        if ___:
            raise TypeError(f"{self.name} must be an int")
        if ___:
            raise ValueError(f"{self.name} must be positive")
        instance.__dict__[self.name] = value


class Stack(Generic[T]):
    """A typed LIFO stack. pop() on an empty stack raises IndexError('pop from empty stack')."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(___)

    def pop(self) -> T:
        if ___:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def __len__(self) -> int:
        return ___


def first_or_none(values: Sequence[T]) -> Optional[T]:
    """Return the first element or None, preserving the element type for type checkers."""
    return ___


class PluginRegistry:
    """Run plugins only by approved name.

    register(name, func) raises ValueError for names not in the allowlist;
    run(name, *args) raises KeyError for unregistered names.
    """

    def __init__(self, allowed: Iterable[str]):
        self._allowed = ___
        self._plugins: dict[str, Callable] = {}

    def register(self, name: str, func: Callable) -> None:
        if ___:
            raise ValueError(f"plugin {name!r} is not allowed")
        self._plugins[name] = func

    def run(self, name: str, *args):
        if ___:
            raise KeyError(name)
        return self._plugins[name](*args)

    def names(self) -> list[str]:
        return ___


def parameter_defaults(func: Callable) -> dict[str, object]:
    """Map each parameter name to its default value, or None if it has no default.

    Hint: inspect.signature(func).parameters and inspect.Parameter.empty.
    """
    return ___


class UserRepository(Protocol):
    """Storage port: anything with get(user_id) and save(user) qualifies."""

    def get(self, user_id: str) -> Optional[dict]: ...
    def save(self, user: dict) -> None: ...


class InMemoryUserRepository:
    """Satisfies UserRepository structurally (no inheritance needed)."""

    def __init__(self) -> None:
        self._users: dict[str, dict] = {}

    def get(self, user_id: str) -> Optional[dict]:
        return ___

    def save(self, user: dict) -> None:
        self._users[user["id"]] = ___


def rename_user(repo: UserRepository, user_id: str, new_name: str) -> dict:
    """Domain service: validate, load, change, save. Raise KeyError if missing,
    ValueError if new_name is blank. Works with any UserRepository."""
    if ___:
        raise ValueError("name cannot be blank")
    user = repo.get(user_id)
    if ___:
        raise KeyError(user_id)
    updated = {**user, "name": new_name.strip()}
    repo.save(updated)
    return updated


@dataclass
class Session:
    """A login session. is_expired() uses an injected clock so tests control time."""
    created_at: datetime
    ttl: timedelta
    clock: Callable[[], datetime] = datetime.now

    def is_expired(self) -> bool:
        return ___


class Vector:
    """2-D vector supporting +, -, * (by a number, either side), abs(), ==, and hashing.

    repr is 'Vector(x, y)'. Unsupported operands return NotImplemented.
    """
    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float):
        self.x, self.y = ___

    def __add__(self, other):
        if ___:
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if ___:
            return NotImplemented
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, factor):
        if ___:
            return NotImplemented
        return Vector(self.x * factor, self.y * factor)

    __rmul__ = __mul__

    def __abs__(self) -> float:
        return ___

    def __eq__(self, other):
        if ___:
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self) -> int:
        return ___

    def __repr__(self) -> str:
        return ___


class LRUCache:
    """Fixed-capacity cache: get() marks a key as recently used; put() evicts the least
    recently used key when full. get() of a missing key returns None. Hint: OrderedDict."""

    def __init__(self, capacity: int):
        from collections import OrderedDict
        if ___:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._data: OrderedDict = OrderedDict()

    def get(self, key):
        if ___:
            return None
        self._data.move_to_end(key)
        return ___

    def put(self, key, value) -> None:
        self._data[key] = value
        self._data.move_to_end(___)
        if ___:
            self._data.popitem(last=False)

    def keys(self) -> list:
        """Keys from least to most recently used."""
        return ___


class Plugin:
    """Base class whose subclasses register themselves by `name` via __init_subclass__.

    Plugin.registry maps name -> subclass. A subclass without a `name` class attribute,
    or with a duplicate name, raises TypeError at class-creation time.
    """
    registry: dict[str, type] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        name = cls.__dict__.get("name")
        if ___:
            raise TypeError(f"{cls.__name__} must define a string `name`")
        if ___:
            raise TypeError(f"duplicate plugin name {name!r}")
        Plugin.registry[name] = cls


def enforce_types(func):
    """Decorator: raise TypeError when an argument is not an instance of its annotation.

    Only check parameters annotated with a plain class (int, str, ...); skip others.
    Hint: inspect.signature(func).bind(*args, **kwargs).
    """
    raise NotImplementedError
