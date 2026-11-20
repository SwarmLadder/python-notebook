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

T = TypeVar("T")


class ReadOnlyBag:
    """A read-only collection supporting len(), iteration, `in` and a safe repr.

    It copies its input so later changes to the caller's list do not leak in.
    repr shows at most 3 items: ReadOnlyBag([1, 2, 3, ...]) for longer bags.
    """

    def __init__(self, items: Iterable):
        self._items = tuple(items)

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator:
        return iter(self._items)

    def __contains__(self, item) -> bool:
        return item in self._items

    def __repr__(self) -> str:
        shown = ", ".join(repr(i) for i in self._items[:3])
        more = ", ..." if len(self._items) > 3 else ""
        return f"ReadOnlyBag([{shown}{more}])"


class Ticket:
    """Ordered by priority (lower first), then by sequence number.

    __eq__ and __lt__ return NotImplemented for non-Ticket operands, and
    Tickets are hashable on (priority, sequence).
    """

    def __init__(self, priority: int, sequence: int, title: str = ""):
        self.priority, self.sequence, self.title = priority, sequence, title

    def _key(self) -> tuple[int, int]:
        return self.priority, self.sequence

    def __eq__(self, other):
        if not isinstance(other, Ticket):
            return NotImplemented
        return self._key() == other._key()

    def __lt__(self, other):
        if not isinstance(other, Ticket):
            return NotImplemented
        return self._key() < other._key()

    def __hash__(self) -> int:
        return hash(self._key())


class PositiveInt:
    """Descriptor that only accepts positive ints (TypeError / ValueError otherwise).

    Usage:  class Order:  quantity = PositiveInt()
    Hint: __set_name__ learns the attribute name; store values in instance.__dict__.
    """

    def __set_name__(self, owner, name: str) -> None:
        self.name = name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value) -> None:
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError(f"{self.name} must be an int")
        if value <= 0:
            raise ValueError(f"{self.name} must be positive")
        instance.__dict__[self.name] = value


class Stack(Generic[T]):
    """A typed LIFO stack. pop() on an empty stack raises IndexError('pop from empty stack')."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def __len__(self) -> int:
        return len(self._items)


def first_or_none(values: Sequence[T]) -> Optional[T]:
    """Return the first element or None, preserving the element type for type checkers."""
    return values[0] if values else None


class PluginRegistry:
    """Run plugins only by approved name.

    register(name, func) raises ValueError for names not in the allowlist;
    run(name, *args) raises KeyError for unregistered names.
    """

    def __init__(self, allowed: Iterable[str]):
        self._allowed = frozenset(allowed)
        self._plugins: dict[str, Callable] = {}

    def register(self, name: str, func: Callable) -> None:
        if name not in self._allowed:
            raise ValueError(f"plugin {name!r} is not allowed")
        self._plugins[name] = func

    def run(self, name: str, *args):
        if name not in self._plugins:
            raise KeyError(name)
        return self._plugins[name](*args)

    def names(self) -> list[str]:
        return sorted(self._plugins)


def parameter_defaults(func: Callable) -> dict[str, object]:
    """Map each parameter name to its default value, or None if it has no default.

    Hint: inspect.signature(func).parameters and inspect.Parameter.empty.
    """
    return {name: (None if p.default is inspect.Parameter.empty else p.default)
            for name, p in inspect.signature(func).parameters.items()}


class UserRepository(Protocol):
    """Storage port: anything with get(user_id) and save(user) qualifies."""

    def get(self, user_id: str) -> Optional[dict]: ...
    def save(self, user: dict) -> None: ...


class InMemoryUserRepository:
    """Satisfies UserRepository structurally (no inheritance needed)."""

    def __init__(self) -> None:
        self._users: dict[str, dict] = {}

    def get(self, user_id: str) -> Optional[dict]:
        return self._users.get(user_id)

    def save(self, user: dict) -> None:
        self._users[user["id"]] = dict(user)


def rename_user(repo: UserRepository, user_id: str, new_name: str) -> dict:
    """Domain service: validate, load, change, save. Raise KeyError if missing,
    ValueError if new_name is blank. Works with any UserRepository."""
    if not new_name.strip():
        raise ValueError("name cannot be blank")
    user = repo.get(user_id)
    if user is None:
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
        return self.clock() >= self.created_at + self.ttl
