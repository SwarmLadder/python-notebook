"""Regression tests for public engineering tickets in project notebooks.

Their starter implementations are deliberately unfinished. Notebook execution
must not imply the independent work passed.
"""
from __future__ import annotations

import pytest

from notebook_runner import ROOT, cell_source, load, run_notebook


@pytest.mark.parametrize("path", [
    "basics/projects/01_calculator.ipynb",
    "intermediate/projects/02_offline_api_etl_pipeline.ipynb",
])
def test_unfinished_project_ticket_does_not_print_passing_grade(path):
    result = run_notebook(ROOT / path)
    assert "Project check: Not attempted" in result.stdout
    assert "Project check: Passed" not in result.stdout


def test_calculator_ticket_is_independent_of_worked_example():
    nb = load(ROOT / "basics/projects/01_calculator.ipynb")
    work = next(c for c in nb["cells"] if c["id"] == "code-018")
    check = next(c for c in nb["cells"] if c["id"] == "code-020")
    assert "raise NotImplementedError" in cell_source(work)
    assert "verify_calculator_ticket" in cell_source(check)
    assert "history == previous" in cell_source(check)
    assert 'operation, 0' in cell_source(check)


def test_pipeline_ticket_verifies_csv_quoting_and_record_preservation():
    nb = load(ROOT / "intermediate/projects/02_offline_api_etl_pipeline.ipynb")
    code = cell_source(next(c for c in nb["cells"] if c["id"] == "code-023"))
    cases = cell_source(next(c for c in nb["cells"] if c["id"] == "code-015"))
    assert "raise NotImplementedError" in code
    assert "csv.DictReader" in code
    assert "entries == original" in code
    assert "test_invalid_row_does_not_drop_next_valid_row" in cases
