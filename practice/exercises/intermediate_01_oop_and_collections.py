# Auto-graded practice. Replace each `raise NotImplementedError` with your code.
# Check your work:  python -m pytest practice -k intermediate_01_oop_and_collections
# Stuck? Re-read the docstring hint, then the lesson notebook it names.
# Reset to a blank copy:  git checkout -- practice/exercises/intermediate_01_oop_and_collections.py

"""Intermediate practice 1 — Comprehensions, classes, dataclasses and properties.

Companion to intermediate/exercises/01_oop_and_collections_exercises.ipynb and
lessons 01–04.
"""
from dataclasses import dataclass, field


def discounted(prices: list[float], percent: float) -> list[float]:
    """Return a NEW list with each price reduced by `percent`, rounded to 2 decimals.

    Raise ValueError for a negative price or a percent outside 0–100.
    Hint: validate first, then transform with a list comprehension.
    """
    raise NotImplementedError('TODO: implement discounted')


def index_by_sku(records: list[dict]) -> dict[str, dict]:
    """Key records by their 'sku'. Raise ValueError on a duplicate SKU.

    Hint: a plain dict comprehension silently overwrites duplicates.
    """
    raise NotImplementedError('TODO: implement index_by_sku')


def unique_usernames(names: list[str]) -> list[str]:
    """Strip + casefold names, drop blank ones, return them sorted and unique."""
    raise NotImplementedError('TODO: implement unique_usernames')


def flatten_grid(rows: list[list[int]]) -> list[int]:
    """Flatten rows in row-major order with a single nested comprehension."""
    raise NotImplementedError('TODO: implement flatten_grid')


def sum_even_squares(n: int) -> int:
    """Sum x*x for even x in range(n) without building a list (use a generator expression)."""
    raise NotImplementedError('TODO: implement sum_even_squares')


class Book:
    """A library book. borrow() raises RuntimeError if already on loan;
    return_book() raises RuntimeError if it is not on loan."""

    def __init__(self, isbn: str, title: str):
        raise NotImplementedError('TODO: implement __init__')

    def borrow(self) -> None:
        raise NotImplementedError('TODO: implement borrow')

    def return_book(self) -> None:
        raise NotImplementedError('TODO: implement return_book')


class Account:
    """A bank account whose balance can only change through deposit/withdraw.

    `balance` is a read-only property. Amounts must be positive (ValueError);
    withdrawing more than the balance raises ValueError and changes nothing.
    """

    def __init__(self, owner: str, balance: float=0):
        raise NotImplementedError('TODO: implement __init__')

    @property
    def balance(self) -> float:
        raise NotImplementedError('TODO: implement balance')

    def deposit(self, amount: float) -> None:
        raise NotImplementedError('TODO: implement deposit')

    def withdraw(self, amount: float) -> None:
        raise NotImplementedError('TODO: implement withdraw')


@dataclass
class Product:
    """A product line. Reject negative price or quantity in __post_init__.

    `total_value` is a property: price * quantity.
    """
    sku: str
    price: float
    quantity: int = 0

    def __post_init__(self):
        raise NotImplementedError('TODO: implement __post_init__')

    @property
    def total_value(self) -> float:
        raise NotImplementedError('TODO: implement total_value')


@dataclass
class Playlist:
    """A playlist that owns its own list of tracks. Hint: field(default_factory=list)."""
    name: str
    tracks: list[str] = field(default_factory=list)

    def add(self, track: str) -> None:
        raise NotImplementedError('TODO: implement add')


@dataclass(frozen=True)
class Coordinate:
    """An immutable, hashable point. Hint: @dataclass(frozen=True)."""
    x: float
    y: float


class Temperature:
    """Stores celsius; exposes a `fahrenheit` property that can be read and set.

    Setting a temperature below absolute zero (-273.15 °C) raises ValueError.
    """

    def __init__(self, celsius: float):
        raise NotImplementedError('TODO: implement __init__')

    @property
    def celsius(self) -> float:
        raise NotImplementedError('TODO: implement celsius')

    @celsius.setter
    def celsius(self, value: float) -> None:
        raise NotImplementedError('TODO: implement celsius')

    @property
    def fahrenheit(self) -> float:
        raise NotImplementedError('TODO: implement fahrenheit')

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        raise NotImplementedError('TODO: implement fahrenheit')


class Inventory:
    """Holds Product objects keyed by SKU; adding an existing SKU raises ValueError."""

    def __init__(self):
        raise NotImplementedError('TODO: implement __init__')

    def add(self, product: Product) -> None:
        raise NotImplementedError('TODO: implement add')

    def total_value(self) -> float:
        raise NotImplementedError('TODO: implement total_value')

    def __len__(self) -> int:
        raise NotImplementedError('TODO: implement __len__')


def transpose(matrix: list[list]) -> list[list]:
    """Swap rows and columns with a nested comprehension: [[1, 2], [3, 4]] -> [[1, 3], [2, 4]]."""
    raise NotImplementedError('TODO: implement transpose')


@dataclass(frozen=True)
class Money:
    """An amount in one currency. `+` adds same-currency amounts (rounded to 2 decimals);
    different currencies raise ValueError. Adding a non-Money returns NotImplemented."""
    amount: float
    currency: str = 'USD'

    def __add__(self, other):
        raise NotImplementedError('TODO: implement __add__')


class Shape:
    """Base class. Subclasses must implement area(); Shape().area() raises NotImplementedError."""

    def area(self) -> float:
        raise NotImplementedError('TODO: implement area')

    def describe(self) -> str:
        """'<ClassName> with area <area to 2 decimals>' — works for every subclass."""
        raise NotImplementedError('TODO: implement describe')


class Rectangle(Shape):
    """A width x height rectangle."""

    def __init__(self, width: float, height: float):
        raise NotImplementedError('TODO: implement __init__')

    def area(self) -> float:
        raise NotImplementedError('TODO: implement area')


class Circle(Shape):
    """A circle with the given radius (use math.pi)."""

    def __init__(self, radius: float):
        raise NotImplementedError('TODO: implement __init__')

    def area(self) -> float:
        raise NotImplementedError('TODO: implement area')


def total_area(shapes: list[Shape]) -> float:
    """Sum the areas of any mix of shapes (polymorphism: just call .area())."""
    raise NotImplementedError('TODO: implement total_area')


class ShoppingCart:
    """Cart of (name -> [unit_price, quantity]). Supports len() (total quantity),
    iteration over item names in insertion order, `in`, and total()."""

    def __init__(self):
        raise NotImplementedError('TODO: implement __init__')

    def add(self, name: str, unit_price: float, quantity: int=1) -> None:
        raise NotImplementedError('TODO: implement add')

    def total(self) -> float:
        raise NotImplementedError('TODO: implement total')

    def __len__(self) -> int:
        raise NotImplementedError('TODO: implement __len__')

    def __iter__(self):
        raise NotImplementedError('TODO: implement __iter__')

    def __contains__(self, name) -> bool:
        raise NotImplementedError('TODO: implement __contains__')
