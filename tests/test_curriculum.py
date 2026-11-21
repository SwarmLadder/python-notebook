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
        name = row["independent_evidence"]
        assert name in cell_source(cells[index]), row["lesson"]
        checks = [cell_source(c) for c in cells[index + 1:] if c.get("id") == "build-check"]
        if checks:
            assert len(checks) == 1 and name in checks[0]
        else:
            assert cell_source(cells[index + 2]) == f"check('{name}')"


@pytest.mark.parametrize("lesson,name,defect", [
    ("06_loops", "scan_batch", lambda events: events.count("A")),
    ("10_functions", "invoice_total",
     lambda lines, fee=0: sum(price * quantity for price, quantity in lines) + fee),
])
def test_pilot_check_rejects_boundary_defect(lesson, name, defect):
    cells = load(ROOT / "basics/notebooks" / f"{lesson}.ipynb")["cells"]
    check = next(cell_source(c) for c in cells if c["id"] == "build-check")
    with pytest.raises(AssertionError):
        exec(check, {name: defect})
