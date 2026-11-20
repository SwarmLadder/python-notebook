"""Every lesson's "Try it" section is fill-in-the-blank with a hidden-answer check."""
import importlib.util
import re

import pytest

from notebook_runner import ROOT, cell_source, load, notebook_id

LEVELS = ("basics", "intermediate", "advanced")
LESSONS = sorted(p for level in LEVELS for p in (ROOT / level / "notebooks").glob("*.ipynb"))
HELPERS = [ROOT / level / "notebooks" / "lesson.py" for level in LEVELS]

spec = importlib.util.spec_from_file_location("lesson_helper", HELPERS[0])
lesson = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lesson)


def test_lesson_helper_is_identical_in_every_level():
    assert len({p.read_text(encoding="utf-8") for p in HELPERS}) == 1


@pytest.mark.parametrize("path", LESSONS, ids=[notebook_id(p) for p in LESSONS])
def test_try_it_exercises_are_fill_in_with_checks(path):
    cells = load(path)["cells"]
    section = [c for c in cells if c.get("id", "").startswith("try-")]
    assert section, "lesson needs a 'Try it' section"
    setup = cell_source(section[1])
    match = re.search(r"Exercises\('([^']+)', (\{.*\})\)", setup)
    assert match, "the first code cell must create Exercises(lesson_id, {number: hash})"
    answers = eval(match.group(2))  # our own literal dict
    exercises = [cell_source(c) for c in section if c["cell_type"] == "code" and "Exercises(" not in cell_source(c)]
    assert len(exercises) == len(answers) >= 3
    for number, code in enumerate(exercises, start=1):
        assert "___" in code, f"exercise {number} has no blank to fill in"
        assert f"check({number}, " in code, f"exercise {number} must end with check({number}, value)"
        assert re.fullmatch(r"[0-9a-f]{16}", answers[number])
    text = "\n".join(cell_source(c) for c in cells)
    assert "TODO" not in text, "no open-ended TODO exercises: write fill-in cells instead"


def test_blank_and_feedback(capsys):
    check = lesson.Exercises("demo", {1: lesson.fingerprint("demo", 1, (1, 2.0))})
    check(1, [1, 2])
    check(1, [2, 1])
    check(1, [lesson.___, 2])
    out = capsys.readouterr().out
    assert "✅" in out and "❌" in out and "fill in every ___" in out
    with pytest.raises(lesson.BlankNotFilled):
        float(lesson.___)


def test_run_works_inside_a_running_event_loop():
    import asyncio

    async def inner():
        return 42

    async def outer():  # simulates Jupyter, where a loop is already running
        return lesson.run(inner())

    assert asyncio.run(outer()) == 42
