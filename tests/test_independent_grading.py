"""Reject partial or interrupted independent assessment runs.

The notebook checker must not infer mastery from one passing test when a
second test failed to collect or the Pytest run exited unsuccessfully.
"""
import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from notebook_runner import ROOT

sys.path.insert(0, str(ROOT / "practice"))
from notebook_check import Checker, tests_by_exercise  # noqa: E402


def report(test, outcome="passed"):
    return SimpleNamespace(
        nodeid=f"practice/tests/test_basics_independent_builds.py::{test}[case]",
        passed=outcome == "passed",
        failed=outcome == "failed",
        skipped=outcome == "skipped",
        when="call", sections=[], longrepr="AssertionError: wrong",
    )


def test_submitted_variable_and_function_names_are_discovered():
    grouped = tests_by_exercise("basics_independent_builds")
    assert "test_session_label" in grouped["session_label"]
    assert "test_receipt" in grouped["receipt"]
    assert "test_invoice_total" in grouped["invoice_total"]


def test_partial_test_coverage_is_not_mastery(capsys):
    checker = Checker("basics_independent_builds")
    expected = ["test_scan_batch", "test_invoice_total"]
    assert checker._report("scan_batch", [report("test_scan_batch")], expected, 0) is False
    assert "Missing test coverage" in capsys.readouterr().out
    assert not checker.passed


@pytest.mark.parametrize("status", [None, 1, 2, 3, 4, 5])
def test_nonzero_or_missing_pytest_exit_is_not_mastery(status):
    checker = Checker("basics_independent_builds")
    assert checker._report("scan_batch", [report("test_scan_batch")], ["test_scan_batch"], status) is False
    assert not checker.passed


def test_later_failure_revokes_earlier_success():
    checker = Checker("basics_independent_builds")
    assert checker._report("scan_batch", [report("test_scan_batch")], ["test_scan_batch"], 0)
    assert "scan_batch" in checker.passed
    assert not checker._report("scan_batch", [report("test_scan_batch", "failed")], ["test_scan_batch"], 1)
    assert "scan_batch" not in checker.passed


def test_incomplete_independent_submissions_never_pass(capsys):
    checker = Checker("advanced_independent_builds")
    assert checker("split_jobs", {}) is False
    assert "split_jobs" not in checker.passed
