"""The auto-graded practice must exist for every workbook and must never leak answers."""
import ast
import json
import re

import pytest

from notebook_runner import ROOT

PRACTICE = ROOT / "practice"
EXERCISES = sorted((PRACTICE / "exercises").glob("*.py"))
WORKBOOKS = sorted(p for level in ("basics", "intermediate", "advanced") for p in (ROOT / level / "exercises").glob("*.ipynb"))
STUB_IDS = [p.stem for p in EXERCISES]


def practice_name(workbook):
    level, number = workbook.parents[1].name, workbook.name.split("_", 1)[0]
    matches = sorted(PRACTICE.glob(f"exercises/{level}_{number}_*.py"))
    return matches[0].stem if matches else None


@pytest.mark.parametrize("workbook", WORKBOOKS, ids=[w.relative_to(ROOT).as_posix() for w in WORKBOOKS])
def test_every_workbook_has_practice_module_tests_and_answer_key(workbook):
    name = practice_name(workbook)
    assert name, f"no practice/exercises/<level>_<nn>_*.py for {workbook.name}"
    assert (PRACTICE / "tests" / f"test_{name}.py").exists()
    assert (PRACTICE / "answers" / f"{name}.json").exists()


def test_no_solutions_folder_is_committed():
    assert not (PRACTICE / "solutions").exists(), "reference solutions must stay private"
    for level in ("basics", "intermediate", "advanced"):
        assert not (ROOT / level / "solutions").exists()


@pytest.mark.parametrize("stub", EXERCISES, ids=STUB_IDS)
def test_stub_contains_no_implementation(stub):
    """Every function body is only a docstring plus `raise NotImplementedError`."""
    leaks = []
    for node in ast.walk(ast.parse(stub.read_text(encoding="utf-8"))):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            body = [n for n in node.body if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant))]
            if not (len(body) == 1 and isinstance(body[0], ast.Raise)):
                leaks.append(node.name)
    assert not leaks, f"stub leaks an implementation: {leaks} (regenerate with tools/make_practice_stubs.py)"


@pytest.mark.parametrize("stub", EXERCISES, ids=STUB_IDS)
def test_every_public_definition_has_a_docstring(stub):
    tree = ast.parse(stub.read_text(encoding="utf-8"))
    missing = [n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
               and not n.name.startswith("_") and not ast.get_docstring(n)]
    assert not missing, f"learners need a docstring to know what to build: {missing}"


@pytest.mark.parametrize("stub", EXERCISES, ids=STUB_IDS)
def test_answer_key_holds_only_fingerprints(stub):
    key = json.loads((PRACTICE / "answers" / f"{stub.stem}.json").read_text(encoding="utf-8"))
    assert key, "empty answer key"
    assert all(re.fullmatch(r"[0-9a-f]{64}", v) for v in key.values()), "answer keys must hold hashes only"


@pytest.mark.parametrize("stub", EXERCISES, ids=STUB_IDS)
def test_every_check_call_has_an_answer(stub):
    """Each test that calls check() has at least one key, so learners never see 'no answer key'."""
    key = json.loads((PRACTICE / "answers" / f"{stub.stem}.json").read_text(encoding="utf-8"))
    tests = ast.parse((PRACTICE / "tests" / f"test_{stub.stem}.py").read_text(encoding="utf-8"))
    recorded = {k.split("[")[0].split("#")[0] for k in key}
    using_check = {n.name for n in tests.body if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")
                   and any(isinstance(c, ast.Call) and getattr(c.func, "id", "") == "check" for c in ast.walk(n))}
    missing = using_check - recorded
    assert not missing, f"rebuild the answer key (missing {sorted(missing)})"


NO_HINT_NEEDED = {"TransientError", "PermanentError", "CircuitOpen", "InvalidQuantity", "UserRepository"}


@pytest.mark.parametrize("stub", EXERCISES, ids=STUB_IDS)
def test_every_exercise_has_step_by_step_hints(stub):
    hints = json.loads((PRACTICE / "hints" / f"{stub.stem}.json").read_text(encoding="utf-8"))
    tree = ast.parse(stub.read_text(encoding="utf-8"))
    names = {n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
             and not n.name.startswith("_")} - NO_HINT_NEEDED
    missing = sorted(n for n in names if len(hints.get(n, [])) < 2)
    assert not missing, f"add two hints (nudge, then method) for: {missing}"
    assert set(hints) <= names | NO_HINT_NEEDED, f"hints for unknown names: {sorted(set(hints) - names)}"
