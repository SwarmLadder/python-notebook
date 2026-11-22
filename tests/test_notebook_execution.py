"""Run every notebook top-to-bottom ("Restart & Run All"), one test per file.

A learner should never hit an error in our own example code. If a test here
fails, the message names the notebook and the failing cell number.
"""
import pytest

from notebook_runner import all_notebooks, notebook_id, run_notebook, _stopped_at_blank

NOTEBOOKS = all_notebooks()


@pytest.mark.parametrize("path", NOTEBOOKS, ids=[notebook_id(p) for p in NOTEBOOKS])
def test_notebook_runs_from_a_fresh_kernel(path):
    result = run_notebook(path)
    assert result.executed_cells > 0, "notebook has no runnable code"


@pytest.mark.parametrize("source, expected", [
    ("___", True),
    ("value = ___ + 1", True),
    ("raise RuntimeError('___')", False),
    ("1 / 0  # ___ is still unanswered elsewhere", False),
    ("missing_name + ___", False),
    ("print('___')\nraise ValueError('broken')", False),
])
def test_only_executed_placeholders_are_skipped(source, expected):
    try:
        exec(compile(source, "<exercise>", "exec"), {})
    except Exception as error:
        assert _stopped_at_blank(error, source) is expected
    else:
        pytest.fail("The fixture should raise")


def test_mixed_exception_group_is_not_treated_as_an_unfinished_blank():
    source = "___"
    try:
        exec(compile(source, "<exercise>", "exec"), {})
    except NameError as error:
        blank = error
    assert _stopped_at_blank(ExceptionGroup("unfinished", [blank]), source)
    assert not _stopped_at_blank(
        ExceptionGroup("mixed", [blank, ValueError("real failure")]), source
    )


def test_chained_real_error_is_not_hidden_by_an_earlier_blank():
    source = "try:\n    ___\nexcept NameError:\n    raise RuntimeError('broken fallback')"
    try:
        exec(compile(source, "<exercise>", "exec"), {})
    except RuntimeError as error:
        assert not _stopped_at_blank(error, source)
    else:
        pytest.fail("The fixture should raise")
