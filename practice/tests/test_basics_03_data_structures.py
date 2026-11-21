import pytest

from grader import check
from practice_loader import module_for

m = module_for(__file__)


def test_evens_does_not_mutate():
    values = [1, 2, 3, 4, 6]
    check(m.evens(values))
    assert values == [1, 2, 3, 4, 6], "the original list must not change"
    check(m.evens([]))


@pytest.mark.parametrize("values, target", [([1, 2, 1, 1], 1), (["a"], "b"), ([], 0)])
def test_count_occurrences(values, target):
    check(m.count_occurrences(values, target))


@pytest.mark.parametrize("values", [[4, 9, 9, 2], [1, 2], [-5, -1, -3]])
def test_second_largest(values):
    check(m.second_largest(values), hint="DISTINCT values: duplicates of the max don't count")


@pytest.mark.parametrize("values", [[], [7], [3, 3, 3]])
def test_second_largest_needs_two_distinct(values):
    with pytest.raises(ValueError):
        m.second_largest(values)


def test_flatten():
    check(m.flatten([[1, 2], [3], [], [4, 5]]))
    check(m.flatten([]))


@pytest.mark.parametrize("point", [(3, 4), (0, 0), (-6, 8)])
def test_distance_from_origin(point):
    check(m.distance_from_origin(point))


def test_unique_cities():
    check(m.unique_cities(["paris", " Paris", "LIMA", "lima "]))
    check(m.unique_cities([]))


def test_compare_sets():
    check(m.compare_sets({1, 2, 3}, {3, 4}))

    assert m.compare_sets(set(), {"A"}) == {"common": set(), "only_a": set(), "only_b": {"A"}}


def test_word_frequencies():
    check(m.word_frequencies("The cat, the hat. THE END!"))
    check(m.word_frequencies(""))


def test_split_pass_fail():
    check(m.split_pass_fail({"Ana": 75, "Ben": 49.5, "Cy": 50}))
    check(m.split_pass_fail({"Ana": 75}, threshold=80))


def test_student_averages():
    check(m.student_averages({"Ana": [90, 85, 77], "Ben": [], "Cy": [100]}))


def test_pairs_to_dict():
    check(m.pairs_to_dict(["a", "b"], [1, 2]))
    check(m.pairs_to_dict([], []))
    with pytest.raises(ValueError):
        m.pairs_to_dict(["a"], [1, 2])


def test_inventory_add_remove():
    inv = m.Inventory()
    inv.add("apple", 5)
    inv.add("apple", 2)
    inv.add("pear", 1)
    check(inv.quantity("apple"))
    inv.remove("apple", 3)
    check(inv.quantity("apple"))
    inv.remove("pear", 1)
    check(inv.items(), hint="items with no stock left should disappear")
    check(inv.quantity("banana"))


def test_inventory_rejects_bad_operations():
    inv = m.Inventory()
    inv.add("apple", 1)
    with pytest.raises(ValueError):
        inv.remove("apple", 2)
    with pytest.raises(ValueError):
        inv.remove("ghost", 1)
    with pytest.raises(ValueError):
        inv.add("apple", 0)
    assert inv.quantity("apple") == 1, "a failed operation must not change stock"


def test_inventories_are_independent():
    first, second = m.Inventory(), m.Inventory()
    first.add("apple", 1)
    assert second.items() == [], "stock must be stored per instance, not shared"


def test_merge_counts_does_not_mutate():
    first, second = {"a": 1, "b": 2}, {"b": 3, "c": 4}
    check(m.merge_counts(first, second))
    assert first == {"a": 1, "b": 2} and second == {"b": 3, "c": 4}, "inputs must not change"

    assert m.merge_counts({}, {}) == {}
    assert m.merge_counts({"A": 2}, {"A": 0, "B": 0}) == {"A": 2, "B": 0}, "Preserve reported zero counts."


def test_invert():
    check(m.invert({"a": 1, "b": 2}))
    with pytest.raises(ValueError):
        m.invert({"a": 1, "b": 1})


@pytest.mark.parametrize("n", [1, 2, 3])
def test_top_words(n):
    check(m.top_words("b a c b a b d", n), hint="ties: alphabetical")


@pytest.mark.parametrize("k", [1, 0, 4, 5, -1])
def test_rotate(k):
    values = [1, 2, 3, 4]
    check(m.rotate(values, k))
    assert values == [1, 2, 3, 4], "return a new list"


def test_rotate_empty():
    check(m.rotate([], 3))

    queue = ["first", "second"]
    rotated = m.rotate(queue, -1)
    assert rotated == ["second", "first"] and queue == ["first", "second"], "Preserve the original queue."
    assert m.rotate(queue, 0) is not queue, "Return a new list even for zero rotation."


@pytest.mark.parametrize("size", [2, 3, 10])
def test_chunk(size):
    check(m.chunk([1, 2, 3, 4, 5], size))


def test_chunk_rejects_zero():
    with pytest.raises(ValueError):
        m.chunk([1], 0)
