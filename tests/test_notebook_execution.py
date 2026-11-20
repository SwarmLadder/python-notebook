"""Run every notebook top-to-bottom ("Restart & Run All"), one test per file.

A learner should never hit an error in our own example code. If a test here
fails, the message names the notebook and the failing cell number.
"""
import pytest

from notebook_runner import all_notebooks, notebook_id, run_notebook

NOTEBOOKS = all_notebooks()


@pytest.mark.parametrize("path", NOTEBOOKS, ids=[notebook_id(p) for p in NOTEBOOKS])
def test_notebook_runs_from_a_fresh_kernel(path):
    result = run_notebook(path)
    if path.parent.name != "exercises":  # exercise workbooks are intentionally blank
        assert result.executed_cells > 0, "notebook has no runnable example code"
