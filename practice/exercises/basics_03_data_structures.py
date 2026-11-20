# Fill in every ___ so the function does what its docstring says.
# Check your work:  python -m pytest practice -k basics_03_data_structures   (or use the workbook notebook)
# Stuck? Fail a check twice to unlock the hints.
# Reset this file:  git checkout -- practice/exercises/basics_03_data_structures.py

"""Basics practice 3 — Lists, tuples, sets and dictionaries.

Companion to basics/exercises/03_data_structures_exercises.ipynb and lessons 07–09.
"""
import string


def evens(values: list[int]) -> list[int]:
    """Return a NEW list containing only the even numbers. Do not modify `values`."""
    return ___


def count_occurrences(values: list, target) -> int:
    """Count how often target appears, using a loop (not list.count)."""
    count = 0
    for value in ___:
        if ___:
            count += 1
    return count


def second_largest(values: list[float]) -> float:
    """Return the second-largest DISTINCT value. Raise ValueError if there is none.

    >>> second_largest([4, 9, 9, 2])
    4
    """
    distinct = sorted(set(values))
    if ___:
        raise ValueError("need at least two distinct values")
    return ___


def flatten(matrix: list[list]) -> list:
    """Flatten a 2-D list with nested loops: [[1, 2], [3]] -> [1, 2, 3]."""
    flat = ___
    for row in ___:
        for item in row:
            flat.append(item)
    return flat


def distance_from_origin(point: tuple[float, float]) -> float:
    """Unpack an (x, y) tuple and return its distance from (0, 0)."""
    x, y = point
    return ___


def unique_cities(cities: list[str]) -> list[str]:
    """Remove duplicates (ignoring case and surrounding spaces) and return sorted title-case names.

    >>> unique_cities(["paris", " Paris", "LIMA"])
    ['Lima', 'Paris']
    """
    return ___


def compare_sets(a: set, b: set) -> dict[str, set]:
    """Return {'common': ..., 'only_a': ..., 'only_b': ...} using set operators."""
    return ___


def word_frequencies(text: str) -> dict[str, int]:
    """Count words case-insensitively, ignoring punctuation.

    >>> word_frequencies("The cat, the hat.")
    {'the': 2, 'cat': 1, 'hat': 1}
    Hint: str.maketrans('', '', string.punctuation) removes punctuation.
    """
    cleaned = ___
    counts: dict[str, int] = {}
    for word in ___:
        counts[word] = counts.get(word, 0) + 1
    return counts


def split_pass_fail(scores: dict[str, float], threshold: float = 50) -> dict[str, dict[str, float]]:
    """Group students into {'pass': {...}, 'fail': {...}}; a score equal to threshold passes."""
    groups: dict[str, dict[str, float]] = {"pass": {}, "fail": {}}
    for name, score in ___:
        groups["pass" if score >= threshold else "fail"][name] = score
    return ___


def student_averages(grades: dict[str, list[float]]) -> dict[str, float]:
    """Map each student to their average grade rounded to 1 decimal; empty lists give 0.0."""
    return ___


def pairs_to_dict(keys: list, values: list) -> dict:
    """Build a dict from two equal-length lists; raise ValueError if lengths differ."""
    if ___:
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
        if ___:
            raise ValueError("quantity must be positive")
        self._stock[item] = self._stock.get(item, 0) + quantity

    def remove(self, item: str, quantity: int) -> None:
        if ___:
            raise ValueError(f"not enough {item}")
        self._stock[item] -= quantity
        if ___:
            del self._stock[item]

    def quantity(self, item: str) -> int:
        return ___

    def items(self) -> list[str]:
        return ___


def merge_counts(first: dict[str, int], second: dict[str, int]) -> dict[str, int]:
    """Add two count dictionaries without changing either input."""
    merged = ___
    for key, value in ___:
        merged[key] = merged.get(key, 0) + value
    return merged


def invert(mapping: dict) -> dict:
    """Swap keys and values. Raise ValueError if two keys share a value."""
    inverted = {}
    for key, value in ___:
        if ___:
            raise ValueError(f"duplicate value: {value!r}")
        inverted[value] = key
    return inverted


def top_words(text: str, n: int) -> list[tuple[str, int]]:
    """The n most common lowercase words as (word, count), most common first;
    ties are broken alphabetically. Hint: sorted(items, key=lambda p: (-p[1], p[0]))."""
    return ___


def rotate(values: list, k: int) -> list:
    """Return a new list rotated right by k places: rotate([1, 2, 3, 4], 1) -> [4, 1, 2, 3].

    k may be larger than the length or negative. Empty lists stay empty.
    """
    if ___:
        return ___
    k %= len(values)
    return values[-k:] + values[:-k]


def chunk(values: list, size: int) -> list[list]:
    """Split into consecutive lists of `size` items; the last may be shorter. size < 1 -> ValueError."""
    if ___:
        raise ValueError("size must be at least 1")
    return [values[i:i + size] for i in range(0, len(values), size)]
