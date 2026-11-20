"""Self-checks for the "Try it" exercises in the lesson notebooks.

Each exercise is a few lines of code with ___ blanks and ends with check(value).
Only a hash of the correct value is stored, so the answer isn't visible, but
your value is still checked. Equivalent answers count: tuple or list, 5 or 5.0,
float differences below 6 decimal places, any order for sets and dicts.

    from lesson import Exercises, ___, run
    check = Exercises("basics/06", {1: "...", 2: "..."})
    check(1, my_value)        # inside exercise 1's cell

`run(coroutine)` runs async code both in Jupyter (which already has an event
loop) and in plain Python.
"""
from __future__ import annotations

import asyncio
import dataclasses
import hashlib
import json
import math
import threading


class BlankNotFilled(Exception):
    """Raised when code uses a ___ blank that hasn't been filled in."""

    def __init__(self):
        super().__init__("✏️  Fill in every ___ blank in this cell, then run it again.")


class _Blank:
    """The ___ placeholder. Any use of it explains what to do instead of a cryptic error."""

    def _stop(self, *args, **kwargs):
        raise BlankNotFilled()

    __call__ = __getattr__ = __getitem__ = __iter__ = __len__ = __bool__ = __index__ = _stop
    __add__ = __radd__ = __sub__ = __rsub__ = __mul__ = __rmul__ = __truediv__ = __rtruediv__ = _stop
    __floordiv__ = __rfloordiv__ = __mod__ = __rmod__ = __pow__ = __rpow__ = __neg__ = _stop
    __lt__ = __le__ = __gt__ = __ge__ = __contains__ = __format__ = __int__ = __float__ = _stop
    __enter__ = __exit__ = __hash__ = _stop

    def __eq__(self, other):
        raise BlankNotFilled()

    def __repr__(self):
        return "___"


_Blank.__name__ = _Blank.__qualname__ = "___"  # so type(___).__name__ also reads as a blank
___ = _Blank()


def _contains_blank(value, depth=0) -> bool:
    if value is ___ or (isinstance(value, str) and value == "___"):
        return True
    if depth > 4:
        return False
    if isinstance(value, (list, tuple, set, frozenset)):
        return any(_contains_blank(v, depth + 1) for v in value)
    if isinstance(value, dict):
        return any(_contains_blank(k, depth + 1) or _contains_blank(v, depth + 1) for k, v in value.items())
    return False


def _norm(value):
    if value is None or isinstance(value, (bool, str)):
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        if math.isnan(value):
            return "nan"
        rounded = round(value, 6) + 0.0
        return int(rounded) if rounded.is_integer() and abs(rounded) < 1e15 else rounded
    if isinstance(value, (list, tuple, range)):
        return [_norm(v) for v in value]
    if isinstance(value, (set, frozenset)):
        return {"set": sorted(json.dumps(_norm(v), sort_keys=True) for v in value)}
    if isinstance(value, dict):
        return {"dict": sorted([json.dumps(_norm(k), sort_keys=True), _norm(v)] for k, v in value.items())}
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        return {f.name: _norm(getattr(value, f.name)) for f in dataclasses.fields(value)}
    return repr(value)


def run(coroutine):
    """asyncio.run() that also works inside Jupyter, where a loop is already running."""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coroutine)
    result = {}

    def target():
        try:
            result["value"] = asyncio.run(coroutine)
        except BaseException as error:  # re-raised in the caller's thread
            result["error"] = error

    worker = threading.Thread(target=target)
    worker.start()
    worker.join()
    if "error" in result:
        raise result["error"]
    return result["value"]


def fingerprint(lesson_id: str, number: int, value) -> str:
    canonical = json.dumps(_norm(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(f"python-notebook-lesson|{lesson_id}|{number}|{canonical}".encode()).hexdigest()[:16]


class Exercises:
    def __init__(self, lesson_id: str, answers: dict[int, str]):
        self.lesson_id = lesson_id
        self._answers = answers
        self.passed: set[int] = set()

    def __call__(self, number: int, value) -> None:
        """Print whether `value` is right. Returns None so Jupyter shows only the message."""
        self.last_result = self._grade(number, value)

    def _grade(self, number: int, value) -> bool | None:
        if number not in self._answers:
            print(f"There is no exercise {number} here.")
            return None
        if _contains_blank(value):
            print(f"✏️  Exercise {number}: fill in every ___ blank first.")
            return None
        if fingerprint(self.lesson_id, number, value) == self._answers[number]:
            self.passed.add(number)
            print(f"✅ Exercise {number}: correct! ({len(self.passed)}/{len(self._answers)} done)")
            return True
        shown = repr(value)
        shown = shown if len(shown) < 200 else shown[:200] + "..."
        print(f"❌ Exercise {number}: not yet. Your result: {shown}\n"
              "   Re-read the example above this section, change one blank, and run the cell again.")
        return False
