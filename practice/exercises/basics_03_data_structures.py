# Auto-graded practice. Replace each `raise NotImplementedError` with your code.
# Check your work:  python -m pytest practice -k basics_03_data_structures
# Stuck? Re-read the docstring hint, then the lesson notebook it names.
# Reset to a blank copy:  git checkout -- practice/exercises/basics_03_data_structures.py

"""Basics practice 3 — Lists, tuples, sets and dictionaries.

Companion to basics/exercises/03_data_structures_exercises.ipynb and lessons 07–09.
"""
import string


def evens(values: list[int]) -> list[int]:
    """Return a NEW list containing only the even numbers. Do not modify `values`."""
    raise NotImplementedError('TODO: implement evens')


def count_occurrences(values: list, target) -> int:
    """Count how often target appears, using a loop (not list.count)."""
    raise NotImplementedError('TODO: implement count_occurrences')


def second_largest(values: list[float]) -> float:
    """Return the second-largest DISTINCT value. Raise ValueError if there is none.

    >>> second_largest([4, 9, 9, 2])
    4
    """
    raise NotImplementedError('TODO: implement second_largest')


def flatten(matrix: list[list]) -> list:
    """Flatten a 2-D list with nested loops: [[1, 2], [3]] -> [1, 2, 3]."""
    raise NotImplementedError('TODO: implement flatten')


def distance_from_origin(point: tuple[float, float]) -> float:
    """Unpack an (x, y) tuple and return its distance from (0, 0)."""
    raise NotImplementedError('TODO: implement distance_from_origin')


def unique_cities(cities: list[str]) -> list[str]:
    """Remove duplicates (ignoring case and surrounding spaces) and return sorted title-case names.

    >>> unique_cities(["paris", " Paris", "LIMA"])
    ['Lima', 'Paris']
    """
    raise NotImplementedError('TODO: implement unique_cities')


def compare_sets(a: set, b: set) -> dict[str, set]:
    """Return {'common': ..., 'only_a': ..., 'only_b': ...} using set operators."""
    raise NotImplementedError('TODO: implement compare_sets')


def word_frequencies(text: str) -> dict[str, int]:
    """Count words case-insensitively, ignoring punctuation.

    >>> word_frequencies("The cat, the hat.")
    {'the': 2, 'cat': 1, 'hat': 1}
    Hint: str.maketrans('', '', string.punctuation) removes punctuation.
    """
    raise NotImplementedError('TODO: implement word_frequencies')


def split_pass_fail(scores: dict[str, float], threshold: float=50) -> dict[str, dict[str, float]]:
    """Group students into {'pass': {...}, 'fail': {...}}; a score equal to threshold passes."""
    raise NotImplementedError('TODO: implement split_pass_fail')


def student_averages(grades: dict[str, list[float]]) -> dict[str, float]:
    """Map each student to their average grade rounded to 1 decimal; empty lists give 0.0."""
    raise NotImplementedError('TODO: implement student_averages')


def pairs_to_dict(keys: list, values: list) -> dict:
    """Build a dict from two equal-length lists; raise ValueError if lengths differ."""
    raise NotImplementedError('TODO: implement pairs_to_dict')


class Inventory:
    """In-memory stock levels.

    add(item, qty) increases stock; remove(item, qty) decreases it and raises
    ValueError if there is not enough stock; quantity(item) returns 0 for unknown
    items; items() returns the sorted names of items with stock > 0.
    """

    def __init__(self):
        raise NotImplementedError('TODO: implement __init__')

    def add(self, item: str, quantity: int) -> None:
        raise NotImplementedError('TODO: implement add')

    def remove(self, item: str, quantity: int) -> None:
        raise NotImplementedError('TODO: implement remove')

    def quantity(self, item: str) -> int:
        raise NotImplementedError('TODO: implement quantity')

    def items(self) -> list[str]:
        raise NotImplementedError('TODO: implement items')


def merge_counts(first: dict[str, int], second: dict[str, int]) -> dict[str, int]:
    """Add two count dictionaries without changing either input."""
    raise NotImplementedError('TODO: implement merge_counts')


def invert(mapping: dict) -> dict:
    """Swap keys and values. Raise ValueError if two keys share a value."""
    raise NotImplementedError('TODO: implement invert')


def top_words(text: str, n: int) -> list[tuple[str, int]]:
    """The n most common lowercase words as (word, count), most common first;
    ties are broken alphabetically. Hint: sorted(items, key=lambda p: (-p[1], p[0]))."""
    raise NotImplementedError('TODO: implement top_words')


def rotate(values: list, k: int) -> list:
    """Return a new list rotated right by k places: rotate([1, 2, 3, 4], 1) -> [4, 1, 2, 3].

    k may be larger than the length or negative. Empty lists stay empty.
    """
    raise NotImplementedError('TODO: implement rotate')


def chunk(values: list, size: int) -> list[list]:
    """Split into consecutive lists of `size` items; the last may be shorter. size < 1 -> ValueError."""
    raise NotImplementedError('TODO: implement chunk')
