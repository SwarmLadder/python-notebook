import pytest

from practice_loader import module_for

m = module_for(__file__)


def test_evens_does_not_mutate():
    values = [1, 2, 3, 4, 6]
    assert m.evens(values) == [2, 4, 6]
    assert values == [1, 2, 3, 4, 6], "the original list must not change"
    assert m.evens([]) == []


def test_count_occurrences():
    assert m.count_occurrences([1, 2, 1, 1], 1) == 3
    assert m.count_occurrences(["a"], "b") == 0


@pytest.mark.parametrize("values, expected", [([4, 9, 9, 2], 4), ([1, 2], 1), ([-5, -1, -3], -3)])
def test_second_largest(values, expected):
    assert m.second_largest(values) == expected


@pytest.mark.parametrize("values", [[], [7], [3, 3, 3]])
def test_second_largest_needs_two_distinct(values):
    with pytest.raises(ValueError):
        m.second_largest(values)


def test_flatten():
    assert m.flatten([[1, 2], [3], [], [4, 5]]) == [1, 2, 3, 4, 5]
    assert m.flatten([]) == []


def test_distance_from_origin():
    assert m.distance_from_origin((3, 4)) == pytest.approx(5)
    assert m.distance_from_origin((0, 0)) == 0


def test_unique_cities():
    assert m.unique_cities(["paris", " Paris", "LIMA", "lima "]) == ["Lima", "Paris"]
    assert m.unique_cities([]) == []


def test_compare_sets():
    result = m.compare_sets({1, 2, 3}, {3, 4})
    assert result == {"common": {3}, "only_a": {1, 2}, "only_b": {4}}


def test_word_frequencies():
    assert m.word_frequencies("The cat, the hat. THE END!") == {"the": 3, "cat": 1, "hat": 1, "end": 1}
    assert m.word_frequencies("") == {}


def test_split_pass_fail():
    result = m.split_pass_fail({"Ana": 75, "Ben": 49.5, "Cy": 50})
    assert result == {"pass": {"Ana": 75, "Cy": 50}, "fail": {"Ben": 49.5}}
    assert m.split_pass_fail({"Ana": 75}, threshold=80) == {"pass": {}, "fail": {"Ana": 75}}


def test_student_averages():
    assert m.student_averages({"Ana": [90, 85, 77], "Ben": [], "Cy": [100]}) == {"Ana": 84.0, "Ben": 0.0, "Cy": 100.0}


def test_pairs_to_dict():
    assert m.pairs_to_dict(["a", "b"], [1, 2]) == {"a": 1, "b": 2}
    assert m.pairs_to_dict([], []) == {}
    with pytest.raises(ValueError):
        m.pairs_to_dict(["a"], [1, 2])


def test_inventory_add_remove():
    inv = m.Inventory()
    inv.add("apple", 5)
    inv.add("apple", 2)
    inv.add("pear", 1)
    assert inv.quantity("apple") == 7
    inv.remove("apple", 3)
    assert inv.quantity("apple") == 4
    inv.remove("pear", 1)
    assert inv.items() == ["apple"], "items with no stock left should disappear"
    assert inv.quantity("banana") == 0


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
