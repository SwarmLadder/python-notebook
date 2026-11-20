"""Every lesson ends with a quiz, and every quiz question has exactly one correct option."""
import importlib.util
import re

import pytest

from notebook_runner import ROOT, cell_source, load, notebook_id

LEVELS = ("basics", "intermediate", "advanced")
LESSONS = sorted(p for level in LEVELS for p in (ROOT / level / "notebooks").glob("*.ipynb"))
QUIZ_FILES = [ROOT / level / "notebooks" / "quiz.py" for level in LEVELS]

spec = importlib.util.spec_from_file_location("quiz_helper", QUIZ_FILES[0])
quiz = importlib.util.module_from_spec(spec)
spec.loader.exec_module(quiz)


def test_quiz_helper_is_identical_in_every_level():
    texts = {path.read_text(encoding="utf-8") for path in QUIZ_FILES}
    assert len(texts) == 1, "keep the three notebooks/quiz.py copies identical"


@pytest.mark.parametrize("path", LESSONS, ids=[notebook_id(p) for p in LESSONS])
def test_lesson_quiz_is_answerable(path):
    cells = {c.get("id"): cell_source(c) for c in load(path)["cells"]}
    assert "quiz-questions" in cells and "quiz-check" in cells, "every lesson needs a Quick quiz"
    match = re.search(r"Quiz\('([^']+)', (\{.*?\})\)", cells["quiz-check"])
    assert match, "quiz cell must create Quiz(id, {number: hash})"
    quiz_id, answers = match.group(1), eval(match.group(2))  # our own literal dict
    questions = re.split(r"\n\*\*(\d+)\.\*\* ", "\n" + cells["quiz-questions"])[1:]
    options = {int(questions[i]): re.findall(r"- \*\*([a-d])\)\*\*", questions[i + 1]) for i in range(0, len(questions), 2)}
    assert set(options) == set(answers), "questions and answer keys don't match"
    for number, letters in options.items():
        hits = [l for l in letters if quiz.fingerprint(quiz_id, number, l) == answers[number]]
        assert len(hits) == 1, f"question {number} must have exactly one correct option"


def test_quiz_feedback(capsys):
    q = quiz.Quiz("demo", {1: quiz.fingerprint("demo", 1, "b")})
    results = []
    for choice in ("?", "a", " B "):
        assert q.answer(1, choice) is None, "answer() prints; returning a value would echo True/False in Jupyter"
        results.append(q.last_result)
    assert results == [None, False, True]
    assert "correct" in capsys.readouterr().out
