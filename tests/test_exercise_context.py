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
