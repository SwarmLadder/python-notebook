"""Check curriculum evidence through the same cells a learner runs."""
import ast
import json

import pytest

import notebook_runner as runner
from notebook_runner import ROOT, cell_source, load

ROWS = json.loads((ROOT / "curriculum/concepts.json").read_text())


def test_map_covers_lessons_and_references_earlier_concepts():
    paths = {p.relative_to(ROOT).as_posix() for p in ROOT.glob("*/notebooks/*.ipynb")}
    assert {row["lesson"] for row in ROWS} == paths
    assert len(ROWS) == len(paths)
    earlier = set()
    for row in ROWS:
        assert row["concept_id"] not in earlier
        assert set(row["prerequisites"] + row["reused_concepts"]) <= earlier
        assert set(row.get("assessed_reuse", [])) <= set(row["reused_concepts"])
        assert row["primary_skill"] and row["difficulty"]
        earlier.add(row["concept_id"])
        cells = load(ROOT / row["lesson"])["cells"]
        ids = [c["id"] for c in cells]
        assert len(ids) == len(set(ids))
        assert ids.index("independent-build") < ids.index("build-work") < ids.index(row["assessment_cell"])
        name = row["independent_evidence"]
        assert name in cell_source(cells[ids.index("independent-build")])
        tree = ast.parse(cell_source(cells[ids.index(row["assessment_cell"])]))
        call = tree.body[-1].value
        assert ast.unparse(call.func) in ("check", "check.assess")
        assert call.args[0].value == name


@pytest.mark.parametrize("row", ROWS, ids=[r["concept_id"] for r in ROWS])
def test_omitted_build_cannot_pass_from_an_earlier_example(row, monkeypatch):
    path = ROOT / row["lesson"]
    notebook = load(path)
    work = next(c for c in notebook["cells"] if c["id"] == "build-work")
    work["source"] = ["# Work removed"]
    monkeypatch.setattr(runner, "load", lambda path: notebook)
    assert not runner.run_notebook(path, assess=row["independent_evidence"]).mastery_passed


@pytest.mark.parametrize("concept,submission,passed", [
    ("b00", "session_label = 'Order Desk'", True),
    ("b04", "receipt = 'pen x 3'", False),
    ("b04", "receipt = '{} x {}'.format(item, units)", True),
    ("b06", "def scan_batch(events): return events.count('A')", False),
    ("b10", "def invoice_total(lines, fee=0): return fee + sum(p*q for p, q in lines)", False),
    ("i03", "def total_area(shapes): return 0", False),
    ("i14", "def test_fee(candidate): pass", False),
    ("a14", "def test_replay(deliver): pass", False),
])
def test_current_saved_submission(concept, submission, passed, monkeypatch):
    row = next(r for r in ROWS if r["concept_id"] == concept)
    path = ROOT / row["lesson"]
    notebook = load(path)
    work = next(c for c in notebook["cells"] if c["id"] == "build-work")
    work["source"] = [submission]
    monkeypatch.setattr(runner, "load", lambda path: notebook)
    result = runner.run_notebook(path, assess=row["independent_evidence"])
    assert result.mastery_passed is passed, result.stdout


def test_early_standard_library_names_are_provided():
    expected = {1: ["math"], 9: ["Counter", "string"], 13: ["Path", "csv", "tempfile"]}
    for number, names in expected.items():
        path = next((ROOT / "basics/notebooks").glob(f"{number:02d}_*.ipynb"))
        setup = cell_source(load(path)["cells"][2])
        imports = {a.asname or a.name for node in ast.walk(ast.parse(setup))
                   if isinstance(node, (ast.Import, ast.ImportFrom)) for a in node.names}
        assert set(names) <= imports


def test_published_inventory_matches_the_lessons():
    import runpy
    stats = runpy.run_path(str(ROOT / "tools/course_stats.py"))["inventory"]()
    readme = (ROOT / "README.md").read_text()
    for row in stats:
        level = row["level"]
        line = next(line for line in readme.splitlines() if f"]({level}/README.md) |" in line)
        fields = [field.strip() for field in line.strip("|").split("|")]
        assert int(fields[1]) == row["lessons"] == row["independent_builds"]
        assert int(fields[3]) == row["named_practice_checks"]
        assert int(fields[5].split()[0]) == row["projects"]


def test_pre_import_lessons_provide_library_setup_and_do_not_assign_imports():
    """Learner exercise cells must not depend on discovering import syntax before Lesson 14."""
    for number in range(14):
        path = next((ROOT / "basics/notebooks").glob(f"{number:02d}_*.ipynb"))
        cells = load(path)["cells"]
        for cell in cells:
            if cell["cell_type"] != "code":
                continue
            cell_id = cell.get("id", "")
            if not (cell_id.startswith(("ex-", "ch-")) or cell_id == "build-work"):
                continue
            tree = ast.parse(cell_source(cell))
            imports = [n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))]
            assert not imports, f"{path.name} {cell_id} asks for an import before imports are taught"


def test_untaught_control_syntax_is_scaffolded():
    basics = ROOT / "basics/notebooks"
    strings = load(next(basics.glob("03_*.ipynb")))
    sets = load(next(basics.glob("08_*.ipynb")))
    strings_code = cell_source(next(c for c in strings["cells"] if c["id"] == "build-work"))
    sets_code = cell_source(next(c for c in sets["cells"] if c["id"] == "build-work"))
    assert "for word in full_name.split():" in strings_code
    assert "'common': ___" in sets_code
    assert "'only_a': ___" in sets_code and "'only_b': ___" in sets_code


@pytest.mark.parametrize("concept,submission", [
    ("b03", "def initials(full_name):\n    parts = full_name.split()\n    return parts[0][0].upper() if parts else ''"),
    ("b08", "def compare_sets(a, b):\n    return {'common': a & b, 'only_a': a - b, 'only_b': a - b}"),
    ("b10", "def invoice_total(lines, fee=0):\n    ordered = any(q > 0 for price, q in lines)\n    amount = sum(price * q for price, q in lines)\n    lines.clear()\n    return amount + fee if ordered else 0"),
    ("i09", "def totals_by_category(rows):\n    totals = {}\n    for row in rows:\n        if row['amount'] > 0:\n            category = row['category']\n            totals[category] = totals.get(category, 0) + row['amount']\n    return totals"),
    ("a19", "def replay_summary(events):\n    first = {}\n    last_conflict = {}\n    accepted = duplicates = conflicts = 0\n    for key, amount in events:\n        if key not in first:\n            first[key] = amount\n            accepted += amount\n        elif first[key] == amount or last_conflict.get(key) == amount:\n            duplicates += 1\n        else:\n            conflicts += 1\n            last_conflict[key] = amount\n    return accepted, duplicates, conflicts"),
])
def test_plausible_but_incorrect_independent_builds_fail(concept, submission, monkeypatch):
    """Do not award mastery to partial behavior or an implementation that mutates inputs."""
    row = next(r for r in ROWS if r["concept_id"] == concept)
    path = ROOT / row["lesson"]
    notebook = load(path)
    next(c for c in notebook["cells"] if c["id"] == "build-work")["source"] = [submission]
    monkeypatch.setattr(runner, "load", lambda path: notebook)
    result = runner.run_notebook(path, assess=row["independent_evidence"])
    assert not result.mastery_passed, result.stdout


@pytest.mark.parametrize("concept", ["b10", "i09", "a19"])
def test_delayed_revisions_have_named_assessed_skills(concept):
    row = next(r for r in ROWS if r["concept_id"] == concept)
    notebook = load(ROOT / row["lesson"])
    prompt = cell_source(next(c for c in notebook["cells"] if c["id"] == "independent-build"))
    assert "Delayed revision" in prompt
    assert row.get("assessed_reuse"), f"{concept} should record independently assessed earlier skills"
    if concept in ("b10", "a19"):
        checks = cell_source(next(c for c in notebook["cells"] if c["id"] == "build-check"))
        assert checks.count("assert ") >= 5
    else:
        practice = (ROOT / "practice/tests/test_intermediate_02_iteration_and_abstractions.py").read_text()
        assert "m.totals_by_category(adjustments)" in practice
