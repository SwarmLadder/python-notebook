# Fill in every ___ so the function does what its docstring says.
# Check your work:  python -m pytest practice -k intermediate_01_oop_and_collections   (or use the workbook notebook)
# Stuck? Fail a check twice to unlock the hints.
# Reset this file:  git checkout -- practice/exercises/intermediate_01_oop_and_collections.py

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
    if ___:
        raise ValueError("percent must be between 0 and 100")
    if ___:
        raise ValueError("prices must be nonnegative")
    return [round(price * (1 - percent / 100), 2) for price in prices]


def index_by_sku(records: list[dict]) -> dict[str, dict]:
    """Key records by their 'sku'. Raise ValueError on a duplicate SKU.

    Hint: a plain dict comprehension silently overwrites duplicates.
    """
    index: dict[str, dict] = {}
    for record in records:
        sku = ___
        if ___:
            raise ValueError(f"duplicate sku: {sku}")
        index[sku] = record
    return index


def unique_usernames(names: list[str]) -> list[str]:
    """Strip + casefold names, drop blank ones, return them sorted and unique."""
    return ___


def flatten_grid(rows: list[list[int]]) -> list[int]:
    """Flatten rows in row-major order with a single nested comprehension."""
    return ___


def sum_even_squares(n: int) -> int:
    """Sum x*x for even x in range(n) without building a list (use a generator expression)."""
    return ___


class Book:
    """A library book. borrow() raises RuntimeError if already on loan;
    return_book() raises RuntimeError if it is not on loan."""

    def __init__(self, isbn: str, title: str):
        self.isbn = ___
        self.title = title
        self.on_loan = False

    def borrow(self) -> None:
        if ___:
            raise RuntimeError(f"{self.title!r} is already on loan")
        self.on_loan = True

    def return_book(self) -> None:
        if ___:
            raise RuntimeError(f"{self.title!r} is not on loan")
        self.on_loan = False


class Account:
    """A bank account whose balance can only change through deposit/withdraw.

    `balance` is a read-only property. Amounts must be positive (ValueError);
    withdrawing more than the balance raises ValueError and changes nothing.
    """

    def __init__(self, owner: str, balance: float = 0):
        if ___:
            raise ValueError("opening balance cannot be negative")
        self.owner = owner
        self._balance = balance

    @property
    def balance(self) -> float:
        return ___

    def deposit(self, amount: float) -> None:
        if ___:
            raise ValueError("deposit must be positive")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        if ___:
            raise ValueError("withdrawal must be positive")
        if ___:
            raise ValueError("insufficient funds")
        self._balance -= amount


@dataclass
class Product:
    """A product line. Reject negative price or quantity in __post_init__.

    `total_value` is a property: price * quantity.
    """
    sku: str
    price: float
    quantity: int = 0

    def __post_init__(self):
        if ___:
            raise ValueError("price and quantity must be nonnegative")

    @property
    def total_value(self) -> float:
        return ___


@dataclass
class Playlist:
    """A playlist that owns its own list of tracks. Hint: field(default_factory=list)."""
    name: str
    tracks: list[str] = field(default_factory=list)

    def add(self, track: str) -> None:
        self.tracks.append(___)


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
        self.celsius = ___

    @property
    def celsius(self) -> float:
        return ___

    @celsius.setter
    def celsius(self, value: float) -> None:
        if ___:
            raise ValueError("below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        return ___

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        self.celsius = ___


class Inventory:
    """Holds Product objects keyed by SKU; adding an existing SKU raises ValueError."""

    def __init__(self):
        self._products: dict[str, Product] = {}

    def add(self, product: Product) -> None:
        if ___:
            raise ValueError(f"duplicate sku: {product.sku}")
        self._products[product.sku] = product

    def total_value(self) -> float:
        return ___

    def __len__(self) -> int:
        return ___


def transpose(matrix: list[list]) -> list[list]:
    """Swap rows and columns with a nested comprehension: [[1, 2], [3, 4]] -> [[1, 3], [2, 4]]."""
    return ___


@dataclass(frozen=True)
class Money:
    """An amount in one currency. `+` adds same-currency amounts (rounded to 2 decimals);
    different currencies raise ValueError. Adding a non-Money returns NotImplemented."""
    amount: float
    currency: str = "USD"

    def __add__(self, other):
        if ___:
            return NotImplemented
        if ___:
            raise ValueError("cannot add different currencies")
        return Money(round(self.amount + other.amount, 2), self.currency)


class Shape:
    """Base class. Subclasses must implement area(); Shape().area() raises NotImplementedError."""

    def area(self) -> float:
        raise NotImplementedError

    def describe(self) -> str:
        """'<ClassName> with area <area to 2 decimals>' — works for every subclass."""
        return ___


class Rectangle(Shape):
    """A width x height rectangle."""

    def __init__(self, width: float, height: float):
        self.width, self.height = ___

    def area(self) -> float:
        return ___


class Circle(Shape):
    """A circle with the given radius (use math.pi)."""

    def __init__(self, radius: float):
        self.radius = ___

    def area(self) -> float:
        import math
        return ___


def total_area(shapes: list[Shape]) -> float:
    """Sum the areas of any mix of shapes (polymorphism: just call .area())."""
    return ___


class ShoppingCart:
    """Cart of (name -> [unit_price, quantity]). Supports len() (total quantity),
    iteration over item names in insertion order, `in`, and total()."""

    def __init__(self):
        self._lines: dict[str, list] = {}

    def add(self, name: str, unit_price: float, quantity: int = 1) -> None:
        if ___:
            raise ValueError("invalid quantity or price")
        line = ___
        line[1] += quantity

    def total(self) -> float:
        return ___

    def __len__(self) -> int:
        return ___

    def __iter__(self):
        return ___

    def __contains__(self, name) -> bool:
        return ___
