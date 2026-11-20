"""Basics practice 3 — Lists, tuples, sets and dictionaries.

Companion to basics/exercises/03_data_structures_exercises.ipynb and lessons 07–09.
"""
import string


def evens(values: list[int]) -> list[int]:
    """Return a NEW list containing only the even numbers. Do not modify `values`."""
    return [v for v in values if v % 2 == 0]


def count_occurrences(values: list, target) -> int:
    """Count how often target appears, using a loop (not list.count)."""
    count = 0
    for value in values:
        if value == target:
            count += 1
    return count


def second_largest(values: list[float]) -> float:
    """Return the second-largest DISTINCT value. Raise ValueError if there is none.

    >>> second_largest([4, 9, 9, 2])
    4
    """
    distinct = sorted(set(values))
    if len(distinct) < 2:
        raise ValueError("need at least two distinct values")
    return distinct[-2]


def flatten(matrix: list[list]) -> list:
    """Flatten a 2-D list with nested loops: [[1, 2], [3]] -> [1, 2, 3]."""
    flat = []
    for row in matrix:
        for item in row:
            flat.append(item)
    return flat


def distance_from_origin(point: tuple[float, float]) -> float:
    """Unpack an (x, y) tuple and return its distance from (0, 0)."""
    x, y = point
    return (x ** 2 + y ** 2) ** 0.5


def unique_cities(cities: list[str]) -> list[str]:
    """Remove duplicates (ignoring case and surrounding spaces) and return sorted title-case names.

    >>> unique_cities(["paris", " Paris", "LIMA"])
    ['Lima', 'Paris']
    """
    return sorted({city.strip().title() for city in cities})


def compare_sets(a: set, b: set) -> dict[str, set]:
    """Return {'common': ..., 'only_a': ..., 'only_b': ...} using set operators."""
    return {"common": a & b, "only_a": a - b, "only_b": b - a}


def word_frequencies(text: str) -> dict[str, int]:
    """Count words case-insensitively, ignoring punctuation.

    >>> word_frequencies("The cat, the hat.")
    {'the': 2, 'cat': 1, 'hat': 1}
    Hint: str.maketrans('', '', string.punctuation) removes punctuation.
    """
    cleaned = text.lower().translate(str.maketrans("", "", string.punctuation))
    counts: dict[str, int] = {}
    for word in cleaned.split():
        counts[word] = counts.get(word, 0) + 1
    return counts


def split_pass_fail(scores: dict[str, float], threshold: float = 50) -> dict[str, dict[str, float]]:
    """Group students into {'pass': {...}, 'fail': {...}}; a score equal to threshold passes."""
    groups: dict[str, dict[str, float]] = {"pass": {}, "fail": {}}
    for name, score in scores.items():
        groups["pass" if score >= threshold else "fail"][name] = score
    return groups


def student_averages(grades: dict[str, list[float]]) -> dict[str, float]:
    """Map each student to their average grade rounded to 1 decimal; empty lists give 0.0."""
    return {name: round(sum(marks) / len(marks), 1) if marks else 0.0
            for name, marks in grades.items()}


def pairs_to_dict(keys: list, values: list) -> dict:
    """Build a dict from two equal-length lists; raise ValueError if lengths differ."""
    if len(keys) != len(values):
        raise ValueError("keys and values must have the same length")
    return dict(zip(keys, values))


class Inventory:
    """In-memory stock levels.

    add(item, qty) increases stock; remove(item, qty) decreases it and raises
    ValueError if there is not enough stock; quantity(item) returns 0 for unknown
    items; items() returns the sorted names of items with stock > 0.
    """

    def __init__(self):
        self._stock: dict[str, int] = {}

    def add(self, item: str, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        self._stock[item] = self._stock.get(item, 0) + quantity

    def remove(self, item: str, quantity: int) -> None:
        if quantity > self._stock.get(item, 0):
            raise ValueError(f"not enough {item}")
        self._stock[item] -= quantity
        if self._stock[item] == 0:
            del self._stock[item]

    def quantity(self, item: str) -> int:
        return self._stock.get(item, 0)

    def items(self) -> list[str]:
        return sorted(self._stock)
