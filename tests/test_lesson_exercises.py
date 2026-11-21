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
def test_lesson_exercises_are_fill_in_with_hidden_answers(path):
    """Lessons teach a little, then test it: every exercise is a fill-in cell checked by hash.

    Works for both layouts: the older "Try it" section at the end, and the
    teach-then-test layout where exercises follow each short section.
    """
    cells = load(path)["cells"]
    sources = [cell_source(c) for c in cells if c["cell_type"] == "code"]
    setup = [s for s in sources if "Exercises(" in s]
    assert len(setup) == 1, "one code cell must create Exercises(lesson_id, {number: hash})"
    match = re.search(r"Exercises\('([^']+)', (\{[^}]*\})", setup[0])
    assert match, "Exercises(lesson_id, {number: hash}) not found"
    answers = eval(match.group(2))  # our own literal dict
    exercises = [s for s in sources if re.search(r"\bcheck\(\d+, ", s)]
    assert len(exercises) == len(answers) >= 3
    for number, code in enumerate(exercises, start=1):
        assert "___" in code, f"exercise {number} has no blank to fill in"
        assert f"check({number}, " in code, f"exercise {number} must end with check({number}, value)"
        assert re.fullmatch(r"[0-9a-f]{16}", answers[number])
    challenges = [s for s in sources if re.fullmatch(r"check\('\w+'\)", s.strip())]
    if challenges:
        assert "practice='" in setup[0], "lessons with challenges name their practice module"
    text = "\n".join(cell_source(c) for c in cells)
    assert "TODO" not in text, "no open-ended TODO exercises: write fill-in cells instead"


def test_challenges_are_graded_by_the_practice_tests(capsys, monkeypatch):
    monkeypatch.delenv("PRACTICE_CHECKS", raising=False)
    check = lesson.Exercises("demo", {}, practice="basics_01_fundamentals")

    def total_cost(price_text, units=7):
        return float(price_text) * units

    namespace = {"total_cost": total_cost}
    assert check._challenge("total_cost", namespace) is True
    assert "✅ total_cost" in capsys.readouterr().out


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


def test_pending_cell_uses_real_blank_names_only():
    assert lesson.pending_exercise("n = ___\ncheck(3, n)") == 3
    assert lesson.pending_exercise("n = '___'\ncheck(3, n)") is None
    assert lesson.pending_exercise("def work(x):\n    return ___") is None


def test_failed_rerun_invalidates_previous_success(capsys, monkeypatch):
    monkeypatch.delenv("PRACTICE_CHECKS", raising=False)
    check = lesson.Exercises("demo", {}, "basics_01_fundamentals", independent="total_cost")
    assert check._challenge("total_cost", {"total_cost": lambda price_text, units=7: float(price_text)*units})
    assert not check._challenge("total_cost", {"total_cost": lambda price_text, units=7: 0})
    assert "total_cost" not in check._checker.passed
    assert "hint 1/" not in capsys.readouterr().out
