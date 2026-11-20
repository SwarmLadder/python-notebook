"""Self-check quizzes for the lesson notebooks.

The correct choices are stored only as short hashes, so you can't see them
by reading this file or the notebook, but your answer can still be checked.

    quiz = Quiz("basics/06", {1: "3f2a...", 2: "...", 3: "..."})
    quiz.answer(1, "b")
"""
from __future__ import annotations

import hashlib


def fingerprint(quiz_id: str, number: int, choice: str) -> str:
    return hashlib.sha256(f"python-notebook-quiz|{quiz_id}|{number}|{choice}".encode()).hexdigest()[:12]


class Quiz:
    def __init__(self, quiz_id: str, answers: dict[int, str]):
        self.quiz_id = quiz_id
        self._answers = answers
        self._correct: set[int] = set()

    def answer(self, number: int, choice: str) -> None:
        """Check your choice ('a', 'b', 'c'...) for question `number`. Prints the result."""
        self.last_result = self._grade(number, choice)

    def _grade(self, number: int, choice: str) -> bool | None:
        if number not in self._answers:
            print(f"There is no question {number}. Questions: {sorted(self._answers)}")
            return None
        choice = str(choice).strip().lower()
        if choice in {"", "?"}:
            print(f"Q{number}: replace '?' with your choice, e.g. quiz.answer({number}, 'a')")
            return None
        if fingerprint(self.quiz_id, number, choice) == self._answers[number]:
            self._correct.add(number)
            print(f"Q{number}: ✅ correct  ({len(self._correct)}/{len(self._answers)} so far)")
            return True
        print(f"Q{number}: ❌ not quite. Re-read the matching section, then try another choice.")
        return False
