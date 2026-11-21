"""Independent engineering acceptance, including mutation-testing tasks."""
import sys
import pytest
from practice_loader import module_for

m = module_for(__file__)


def test_environment_report():
    result = m.environment_report()
    assert type(result) is dict
    assert result == {"major": sys.version_info.major, "minor": sys.version_info.minor}
    assert all(type(value) is int for value in result.values()), "Report integers, not version text"


def _conforming_fee(units, fee):
    return fee if units > 0 else 0


def _bill_empty(units, fee):
    return fee


def _multiply_fee(units, fee):
    return units * fee


def _zero_is_positive(units, fee):
    return fee if units >= 0 else 0


def test_test_fee():
    m.test_fee(_conforming_fee)
    for faulty in (_bill_empty, _multiply_fee, _zero_is_positive):
        with pytest.raises(AssertionError):
            m.test_fee(faulty)


@pytest.mark.parametrize("catalog,queries,expected", [
    (["A", "B", "A"], ["A", "B", "X"], [1, 2, 3]),
    ([], ["X"], [0]), (["A"], [], []),
    (["X", "A", "A"], ["A", "X", "Y"], [2, 1, 3]),
    (["A", "A"], ["A"], [1]),
])
def test_lookup_counts(catalog, queries, expected):
    before, requested = catalog[:], queries[:]
    assert m.lookup_counts(catalog, queries) == expected, "Stop at the FIRST match, or after a full miss"
    assert catalog == before and queries == requested, "Do not change caller inputs"


@pytest.mark.parametrize("expected,received,result", [
    ({"A": 2, "B": 1}, {"B": 1, "C": 3}, {"A": -2, "C": 3}),
    ({}, {}, {}), ({"A": 0}, {"A": 0}, {}),
    ({"X": 5}, {}, {"X": -5}),
    ({}, {"Y": 2}, {"Y": 2}),
    ({"A": 4, "B": 3}, {"A": 4, "B": 0}, {"B": -3}),
])
def test_reconcile(expected, received, result):
    left, right = expected.copy(), received.copy()
    assert m.reconcile(expected, received) == result, "Return only nonzero received-minus-expected deltas"
    assert expected == left and received == right, "Preserve both input mappings"
