"""Check isolated submissions without borrowing names from unrelated demonstrations."""
import ast
import builtins
import symtable

import pytest

from notebook_runner import ROOT, cell_source, load
from exercise_context import selected_cells


def global_reads(scope):
    names = {s.get_name() for s in scope.get_symbols() if s.is_global() and s.is_referenced()}
    for child in scope.get_children():
        names.update(global_reads(child))
    return names


@pytest.mark.parametrize("path", sorted(ROOT.glob("*/notebooks/*.ipynb")), ids=lambda p: p.stem)
def test_declared_context_provides_starter_globals(path):
    notebook = load(path)
    for cell in notebook["cells"]:
        key = cell["id"]
        if cell["cell_type"] != "code" or not (key.startswith(("ex-", "ch-")) or key == "build-work"):
            continue
        available = set(dir(builtins))
        context = selected_cells(notebook, key)
        for part in context:
            scope = symtable.symtable(cell_source(part), part["id"], "exec")
            available.update(s.get_name() for s in scope.get_symbols() if s.is_assigned() or s.is_imported())
        assert not (missing := global_reads(scope) - available), f"{path.name}#{key}: {missing}"


def test_no_comprehensions_before_the_lists_explanation():
    for path in sorted((ROOT / "basics/notebooks").glob("*.ipynb"))[:8]:
        for cell in load(path)["cells"]:
            if path.name.startswith("07_") and cell["id"] == "teach-3":
                break
            if cell["cell_type"] == "code":
                assert not any(isinstance(n, ast.comprehension) for n in ast.walk(ast.parse(cell_source(cell)))), (path.name, cell["id"])


@pytest.mark.parametrize("concept, number, correct, alternative, wrong", [
    ("intermediate/15", 6,
     'return [r[0] for r in conn.execute("SELECT title FROM tasks ORDER BY id")]',
     'return list(map(lambda row: row[0], conn.execute("SELECT title FROM tasks ORDER BY id")))',
     'return sorted(r[0] for r in conn.execute("SELECT title FROM tasks"))'),
    ("advanced/18", 6,
     'value = int(settings.get("APP_WORKERS", 4))\n    if value < 1: raise ValueError\n    return value',
     'value = int(settings["APP_WORKERS"]) if "APP_WORKERS" in settings else 4\n    if value <= 0: raise ValueError\n    return value',
     'return max(1, int(settings.get("APP_WORKERS", 4)))'),
])
def test_component_reruns_exact_editor_source(concept, number, correct, alternative, wrong, monkeypatch):
    level, prefix = concept.split("/")
    path = next((ROOT / level / "notebooks").glob(prefix + "_*.ipynb"))
    monkeypatch.syspath_prepend(str(path.parent))
    monkeypatch.chdir(path.parent)
    ns = {"__name__": "__main__"}
    *setup, work = selected_cells(load(path), f"ex-{number}")
    for cell in setup:
        exec(compile(cell_source(cell), cell["id"], "exec", dont_inherit=True), ns)
    code = cell_source(work)
    for solution, expected in [(None, None), (correct, True), (alternative, True), (wrong, False)]:
        edited = code if solution is None else code.replace("raise NotImplementedError", solution, 1)
        exec(compile(edited, work["id"], "exec", dont_inherit=True), ns)
        assert ns["check"].last_result is expected
        assert (number in ns["check"].passed) == (expected is True)


def test_repaired_component_requires_a_discriminating_regression(monkeypatch):
    path = next((ROOT / "advanced/notebooks").glob("16_*.ipynb"))
    monkeypatch.chdir(path.parent)
    monkeypatch.syspath_prepend(str(path.parent))
    ns = {"__name__": "__main__"}
    *setup, work = selected_cells(load(path), "ex-7")
    for cell in setup:
        exec(cell_source(cell), ns)
    source = cell_source(work)
    repair = source.replace("return actual >= minimum",
                            "return tuple(map(int, actual.split('.'))) >= tuple(map(int, minimum.split('.')))", 1)
    for test, expected in [("pass", False), ('assert candidate("1.11.0", "1.9.0")', True),
                           ('assert not candidate("1.2.0", "1.2.0")', False)]:
        exec(repair.replace("raise NotImplementedError", test), ns)
        assert ns["check"].last_result is expected


def test_sqlite_submission_runs_as_a_standalone_module(tmp_path):
    import subprocess
    import sys

    path = ROOT / "intermediate/notebooks/15_sqlite_and_transactions.ipynb"
    cells = selected_cells(load(path), "build-work")
    setup = ast.parse(cell_source(cells[1]))
    imports = [ast.unparse(n) for n in setup.body if isinstance(n, (ast.Import, ast.ImportFrom))
               and getattr(n, "module", None) != "lesson"]
    function = cell_source(cells[-1]).replace("raise NotImplementedError",
        'return dict(open=conn.execute("SELECT COUNT(*) FROM tasks WHERE done=0").fetchone()[0], '
        'done=conn.execute("SELECT COUNT(*) FROM tasks WHERE done=1").fetchone()[0])')
    (tmp_path / "report.py").write_text("\n".join(imports) + "\n" + function)
    (tmp_path / "cli.py").write_text(
        'import sqlite3\nfrom report import count_by_status\n'
        'with sqlite3.connect(":memory:") as db:\n'
        '    db.execute("CREATE TABLE tasks(done INTEGER)")\n'
        '    db.execute("INSERT INTO tasks VALUES (1)")\n'
        '    assert count_by_status(db) == {"open": 0, "done": 1}\n')
    subprocess.run([sys.executable, "cli.py"], cwd=tmp_path, check=True)
