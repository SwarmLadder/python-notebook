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
    if not 0 <= percent <= 100:
        raise ValueError("percent must be between 0 and 100")
    if any(price < 0 for price in prices):
        raise ValueError("prices must be nonnegative")
    return [round(price * (1 - percent / 100), 2) for price in prices]


def index_by_sku(records: list[dict]) -> dict[str, dict]:
    """Key records by their 'sku'. Raise ValueError on a duplicate SKU.

    Hint: a plain dict comprehension silently overwrites duplicates.
    """
    index: dict[str, dict] = {}
    for record in records:
        sku = record["sku"]
        if sku in index:
            raise ValueError(f"duplicate sku: {sku}")
        index[sku] = record
    return index


def unique_usernames(names: list[str]) -> list[str]:
    """Strip + casefold names, drop blank ones, return them sorted and unique."""
    return sorted({name.strip().casefold() for name in names if name.strip()})


def flatten_grid(rows: list[list[int]]) -> list[int]:
    """Flatten rows in row-major order with a single nested comprehension."""
    return [value for row in rows for value in row]


def sum_even_squares(n: int) -> int:
    """Sum x*x for even x in range(n) without building a list (use a generator expression)."""
    return sum(x * x for x in range(0, n, 2))


class Book:
    """A library book. borrow() raises RuntimeError if already on loan;
    return_book() raises RuntimeError if it is not on loan."""

    def __init__(self, isbn: str, title: str):
        self.isbn = isbn
        self.title = title
        self.on_loan = False

    def borrow(self) -> None:
        if self.on_loan:
            raise RuntimeError(f"{self.title!r} is already on loan")
        self.on_loan = True

    def return_book(self) -> None:
        if not self.on_loan:
            raise RuntimeError(f"{self.title!r} is not on loan")
        self.on_loan = False


class Account:
    """A bank account whose balance can only change through deposit/withdraw.

    `balance` is a read-only property. Amounts must be positive (ValueError);
    withdrawing more than the balance raises ValueError and changes nothing.
    """

    def __init__(self, owner: str, balance: float = 0):
        if balance < 0:
            raise ValueError("opening balance cannot be negative")
        self.owner = owner
        self._balance = balance

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("withdrawal must be positive")
        if amount > self._balance:
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
        if self.price < 0 or self.quantity < 0:
            raise ValueError("price and quantity must be nonnegative")

    @property
    def total_value(self) -> float:
        return self.price * self.quantity


@dataclass
class Playlist:
    """A playlist that owns its own list of tracks. Hint: field(default_factory=list)."""
    name: str
    tracks: list[str] = field(default_factory=list)

    def add(self, track: str) -> None:
        self.tracks.append(track)


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
        self.celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError("below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        return self.celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        self.celsius = (value - 32) * 5 / 9


class Inventory:
    """Holds Product objects keyed by SKU; adding an existing SKU raises ValueError."""

    def __init__(self):
        self._products: dict[str, Product] = {}

    def add(self, product: Product) -> None:
        if product.sku in self._products:
            raise ValueError(f"duplicate sku: {product.sku}")
        self._products[product.sku] = product

    def total_value(self) -> float:
        return sum(p.total_value for p in self._products.values())

    def __len__(self) -> int:
        return len(self._products)
