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



def test_running_totals_have_consistent_prompt_starter_and_fingerprint(capsys):
    import ast
    from notebook_runner import cell_source, load
    book = load(ROOT / "basics/notebooks/16_basic_problem_solving.ipynb")
    cells = {cell["id"]: cell_source(cell) for cell in book["cells"]}
    prompt, code, setup = (cells["ex-2-q"], cells["ex-2"], cells["lesson-setup"])
    assert "[1, 2, 3, 4]" in prompt and "[1, 3, 6, 10]" in prompt
    assert code.startswith("values = [1, 2, 3, 4]\n")
    assert "    running.append(___)\n" in code  # Indentation is part of the starter.
    assert lesson.pending_exercise(code) == 2
    match = re.search(r"Exercises\('basics/16', (\{[^}]+\})", setup)
    assert match is not None
    answers = ast.literal_eval(match.group(1))
    assert answers[2] == lesson.fingerprint("basics/16", 2, [1, 3, 6, 10])


def test_running_total_feedback_without_ipython_transformer(capsys):
    """Exercise execution in a basic exec environment mirrors the browser's fallback."""
    from notebook_runner import cell_source, load
    book = load(ROOT / "basics/notebooks/16_basic_problem_solving.ipynb")
    code = cell_source(next(c for c in book["cells"] if c["id"] == "ex-2"))
    expected = [1, 3, 6, 10]
    check = lesson.Exercises("basics/16", {2: lesson.fingerprint("basics/16", 2, expected)})
    check.hints = {2: [
        "Your total changes, but where do you save each updated value?",
        "Lists have a method for adding an element at the end.",
        "After updating total, add its current value to running.",
    ]}
    state = {"check": check, "___": lesson.___}

    # Run the untouched cell without any IPython input transformer: no false failure.
    exec(code, state)
    assert check.last_result is None and 2 not in check.passed
    assert "Not attempted" in capsys.readouterr().out

    wrong = code.replace("running.append(___)", "running.append(0)")
    for hint in check.hints[2]:
        exec(wrong, state)
        output = capsys.readouterr().out
        assert "Needs improvement" in output and hint in output
        assert 2 not in check.passed

    # The intended answer and an equivalent list operation must both pass.
    for answer in ("running.append(total)", "running += [total]"):
        exec(code.replace("running.append(___)", answer), state)
        assert check.last_result is True and 2 in check.passed
        assert "Passed" in capsys.readouterr().out

    # Editing a previously passing solution invalidates the recorded pass.
    exec(wrong, state)
    assert check.last_result is False and 2 not in check.passed
    assert "Needs improvement" in capsys.readouterr().out


def test_placeholder_detection_ignores_comments_and_literal_strings(capsys):
    assert lesson.pending_exercise(
        "# ___ is just a comment\ntext = '___'\ncheck(2, text)"
    ) is None
    assert lesson.pending_exercise(
        'text = "___"  # comment ___\ncheck(2, text)'
    ) is None
    assert lesson.pending_exercise(
        "x = ___  # real blank\ncheck(2, x)"
    ) == 2
    check = lesson.Exercises("text", {1: lesson.fingerprint("text", 1, "___")})
    check(1, "___")
    assert check.last_result is True
    assert "Passed" in capsys.readouterr().out
