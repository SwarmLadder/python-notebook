"""Structural quality checks, one test per notebook per rule.

These keep every notebook easy to learn from: it opens in Jupyter, has a clear
title and learning goals, contains no stale outputs, and has valid Python.
"""
import re

import pytest

from notebook_runner import all_notebooks, cell_source, load, notebook_id, syntax_errors

NOTEBOOKS = all_notebooks()
IDS = [notebook_id(p) for p in NOTEBOOKS]


def test_course_has_notebooks():
    assert len(NOTEBOOKS) >= 75, "notebook discovery looks broken"


@pytest.mark.parametrize("path", NOTEBOOKS, ids=IDS)
def test_is_valid_nbformat4(path):
    nb = load(path)
    assert nb.get("nbformat") == 4
    assert isinstance(nb.get("cells"), list) and nb["cells"], "notebook has no cells"
    assert nb.get("metadata", {}).get("kernelspec", {}).get("language") == "python"
    for cell in nb["cells"]:
        assert cell.get("cell_type") in {"markdown", "code", "raw"}


@pytest.mark.parametrize("path", NOTEBOOKS, ids=IDS)
def test_code_cells_have_valid_syntax(path):
    errors = syntax_errors(load(path), notebook_id(path))
    assert not errors, "\n".join(errors)


@pytest.mark.parametrize("path", NOTEBOOKS, ids=IDS)
def test_starts_with_a_title(path):
    first = load(path)["cells"][0]
    assert first["cell_type"] == "markdown", "first cell should introduce the notebook"
    assert cell_source(first).lstrip().startswith("# "), "first cell should start with a '# Title'"


@pytest.mark.parametrize("path", NOTEBOOKS, ids=IDS)
def test_has_explanations_not_only_code(path):
    cells = load(path)["cells"]
    markdown = sum(c["cell_type"] == "markdown" for c in cells)
    assert markdown >= 3, "learning notebooks need explanatory Markdown between code cells"


@pytest.mark.parametrize("path", NOTEBOOKS, ids=IDS)
def test_outputs_are_cleared(path):
    """Committed outputs go stale and spoil 'predict before you run'."""
    dirty = [n for n, c in enumerate(load(path)["cells"], start=1)
             if c["cell_type"] == "code" and (c.get("outputs") or c.get("execution_count"))]
    assert not dirty, f"clear outputs before committing (cells {dirty})"


LESSONS = [p for p in NOTEBOOKS if p.parent.name == "notebooks"]


@pytest.mark.parametrize("path", LESSONS, ids=[notebook_id(p) for p in LESSONS])
def test_lessons_include_practice(path):
    text = "\n".join(cell_source(c) for c in load(path)["cells"]).lower()
    assert re.search(r"exercise|practice|challenge|self-check|check your understanding", text), \
        "every lesson should give the learner something to try"


EXERCISES = [p for p in NOTEBOOKS if p.parent.name == "exercises"]


@pytest.mark.parametrize("path", EXERCISES, ids=[notebook_id(p) for p in EXERCISES])
def test_exercise_workbooks_link_to_autograded_practice(path):
    text = "\n".join(cell_source(c) for c in load(path)["cells"])
    assert "practice/" in text, "exercise workbooks should point to their auto-graded practice module"


@pytest.mark.parametrize("path", NOTEBOOKS, ids=IDS)
def test_no_links_to_removed_solutions(path):
    text = "\n".join(cell_source(c) for c in load(path)["cells"])
    assert "solutions/" not in text, "reference solutions are private; do not link to them"


LESSON_IDS = [notebook_id(p) for p in LESSONS]


@pytest.mark.parametrize("path", LESSONS, ids=LESSON_IDS)
def test_lessons_end_with_a_next_step(path):
    last = cell_source(load(path)["cells"][-1])
    assert last.startswith("**Next:**"), "end each lesson with a **Next:** link"


@pytest.mark.parametrize("path", NOTEBOOKS, ids=IDS)
def test_first_code_cell_is_the_colab_setup(path):
    """Colab opens one notebook alone; the setup cell fetches the helpers and data it needs."""
    import sys
    sys.path.insert(0, str(path.parents[2] / "tools"))
    from colab_setup import setup_code
    code_cells = [c for c in load(path)["cells"] if c["cell_type"] == "code"]
    assert code_cells and cell_source(code_cells[0]) == setup_code(path.parts[-3], path.parts[-2]), \
        "first code cell must be tools/colab_setup.setup_code(level, folder)"
