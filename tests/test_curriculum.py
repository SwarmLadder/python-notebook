"""Check the map and the independent-build cells used by learners."""
import json

import pytest

from notebook_runner import ROOT, cell_source, load


def test_map_covers_lessons_and_references_earlier_concepts():
    rows = json.loads((ROOT / "curriculum/concepts.json").read_text())
    paths = {p.relative_to(ROOT).as_posix() for p in ROOT.glob("*/notebooks/*.ipynb")}
    assert {row["lesson"] for row in rows} == paths
    assert len(rows) == len(paths)
    earlier = set()
    for row in rows:
        assert row["concept_id"] not in earlier
        assert set(row["prerequisites"] + row["reused_concepts"]) <= earlier
        assert row["primary_skill"] and row["difficulty"]
        earlier.add(row["concept_id"])
        cells = load(ROOT / row["lesson"])["cells"]
        builds = [i for i, cell in enumerate(cells) if cell.get("id") == "independent-build"]
        assert len(builds) == 1, row["lesson"]
        index = builds[0]
        # Map each build to a real practice-module test for achievement evidence.
        import ast
        module = row["mastery_module"]
        assert module.startswith(row["lesson"].split("/")[0] + "_")
        submission = ROOT / "practice" / "exercises" / f"{module}.py"
        tests = ROOT / "practice" / "tests" / f"test_{module}.py"
        assert submission.is_file() and tests.is_file(), row["lesson"]
        name = row["independent_evidence"]
        tree = ast.parse(submission.read_text(encoding="utf-8"))
        definitions = {n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
        definitions.update(target.id for n in tree.body if isinstance(n, ast.Assign)
                           for target in n.targets if isinstance(target, ast.Name))
        assert name in definitions, row["lesson"]
        tested = ast.parse(tests.read_text(encoding="utf-8"))
        assert any(isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name)
                   and n.value.id == "m" and n.attr == name for n in ast.walk(tested)), row["lesson"]
        assert set(row["independently_reinforced"]) <= set(row["reused_concepts"])
        name = row["independent_evidence"]
        assert name in cell_source(cells[index]), row["lesson"]
        checks = [cell_source(c) for c in cells[index + 1:] if c.get("id") == "build-check"]
        if checks:
            assert len(checks) == 1 and name in checks[0]
        else:
            assert cell_source(cells[index + 2]) == f"check('{name}')"


@pytest.mark.parametrize("name,defect", [
    ("scan_batch", lambda events: events.count("A")),
    ("invoice_total", lambda lines, fee=0: sum(price * qty for price, qty in lines) + fee),
])
def test_independent_build_rejects_plausible_boundary_defects(name, defect):
    """Exercise a real practice-route check, not only handpicked inline asserts."""
    import sys
    sys.path.insert(0, str(ROOT / "practice"))
    from notebook_check import Checker

    checker = Checker("basics_independent_builds")
    assert checker(name, {name: defect}) is False
    assert name not in checker.passed
