"""Every exercise workbook has an auto-graded practice module, and its stub is in sync."""
import ast
import subprocess
import sys

import pytest

from notebook_runner import ROOT

PRACTICE = ROOT / "practice"
SOLUTIONS = sorted((PRACTICE / "solutions").glob("*.py"))
WORKBOOKS = sorted(p for level in ("basics", "intermediate", "advanced") for p in (ROOT / level / "exercises").glob("*.ipynb"))


def practice_name(workbook):
    level = workbook.parents[1].name
    number = workbook.name.split("_", 1)[0]
    matches = sorted(PRACTICE.glob(f"solutions/{level}_{number}_*.py"))
    return matches[0].stem if matches else None


@pytest.mark.parametrize("workbook", WORKBOOKS, ids=[w.relative_to(ROOT).as_posix() for w in WORKBOOKS])
def test_every_workbook_has_practice_module_and_tests(workbook):
    name = practice_name(workbook)
    assert name, f"no practice/solutions/<level>_<nn>_*.py for {workbook.name}"
    assert (PRACTICE / "exercises" / f"{name}.py").exists()
    assert (PRACTICE / "tests" / f"test_{name}.py").exists()


@pytest.mark.parametrize("solution", SOLUTIONS, ids=[s.stem for s in SOLUTIONS])
def test_every_public_function_has_a_docstring(solution):
    tree = ast.parse(solution.read_text(encoding="utf-8"))
    missing = [node.name for node in tree.body
               if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
               and not node.name.startswith("_") and not ast.get_docstring(node)]
    assert not missing, f"learners need a docstring to know what to build: {missing}"


def test_stubs_are_up_to_date():
    result = subprocess.run([sys.executable, "tools/make_practice_stubs.py", "--check"],
                            cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
