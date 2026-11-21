"""Behavioral acceptance tests for notebook-only Basics builds.

These test observable results, not solution structure or a reference algorithm.
"""
import pytest
from practice_loader import module_for

m = module_for(__file__)


def test_session_label():
    if m.session_label is None:
        raise NotImplementedError("Complete Basics 00 independent build")
    assert m.session_label == "Order Desk"


def test_receipt():
    if m.receipt is None:
        raise NotImplementedError("Complete Basics 04 independent build")
    assert m.receipt == "pen x 3"


@pytest.mark.parametrize("events, expected", [
    ("AxA|AA", 2), ("|AAA", 0), ("A|AAA", 1),
    ("aAAA", 3), ("", 0), ("A|A|A", 1), ("AAa", 2),
])
def test_scan_batch(events, expected):
    assert m.scan_batch(events) == expected, f"Scanner must stop at first |: {events!r}"


@pytest.mark.parametrize("lines,fee,expected", [
    ([], 5, 0), ([(2, 0)], 7, 0), ([(0, 1)], 7, 7),
    ([(120, 3), (50, 2)], 10, 470),
    ([(2, 0), (3, 1)], 4, 7), ([(25, 2)], 0, 50),
])
def test_invoice_total(lines, fee, expected):
    before = lines[:]
    assert m.invoice_total(lines, fee) == expected, "Charge the fee once, only when units are ordered"
    assert lines == before, "Do not modify the caller's order"


@pytest.mark.parametrize("stock,target,expected", [
    ([5, 3, 1], 3, 2), ([3], 3, None), ([], 2, None),
    ([1, 0, 2], 1, 1), ([0, 0, 2], 0, None),
    ([-1, 0], 0, 0), ([2, 2], 2, None),
])
def test_first_shortfall(stock, target, expected):
    before = stock[:]
    assert m.first_shortfall(stock, target) == expected, "Exactly at target is not a shortfall"
    assert stock == before, "Do not modify the stock counts"


@pytest.mark.parametrize("events,expected", [
    ("AAABBAC", [("A", 3), ("B", 2), ("A", 1), ("C", 1)]),
    ("", []), ("A", [("A", 1)]),
    ("ABAB", [("A", 1), ("B", 1), ("A", 1), ("B", 1)]),
    ("AAAA", [("A", 4)]),
])
def test_pack_runs(events, expected):
    assert m.pack_runs(events) == expected, "Preserve consecutive groups, not just global counts"


@pytest.mark.parametrize("rows,expected", [
    ([], ({}, 0)),
    ([("A", "2"), ("B", " 3 "), ("A", "4"), ("Z", "0"),
      ("X", "-1"), ("R", "oops"), ("B", "1")],
     ({"A": 6, "B": 4, "Z": 0}, 2)),
    ([("A", ""), ("A", "2.0"), ("A", "0"), ("A", None)],
     ({"A": 0}, 3)),
    ([("x", "-2"), ("y", "4")], ({"y": 4}, 1)),
])
def test_stock_report(rows, expected):
    before = rows[:]
    assert m.stock_report(rows) == expected, "Count bad rows without dropping valid zero quantities"
    assert rows == before, "Do not modify the input rows"
