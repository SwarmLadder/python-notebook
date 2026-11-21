"""Hidden-answer grading for the practice modules.

Tests call ``check(value)`` instead of ``assert value == <answer>``. The repo
stores only a salted SHA-256 fingerprint of each correct value in
practice/answers/<module>.json, so neither the solution code nor the expected
outputs are visible. Your value is fingerprinted the same way and compared.

Values are normalized first, so equivalent answers match: tuples and lists are
the same, 5 and 5.0 are the same, floats are compared to 6 decimal places, and
sets and dicts ignore order. True and 1 stay different.
"""
from __future__ import annotations

import dataclasses
import hashlib
import inspect
import json
import math
import os
from collections import defaultdict
from pathlib import Path

ANSWERS_DIR = Path(__file__).resolve().parent / "answers"
SALT = "python-notebook-practice/v1"

SHOW_HINTS = True
RECORDING = False  # set by conftest when a maintainer rebuilds the answer keys
_keys: dict[str, dict[str, str]] = {}
_recorded: dict[str, dict[str, str]] = defaultdict(dict)
_counters: dict[str, int] = defaultdict(int)


def _norm(value):
    if value is None or isinstance(value, (bool, str)):
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        if math.isnan(value):
            return "nan"
        if math.isinf(value):
            return "inf" if value > 0 else "-inf"
        rounded = round(value, 6) + 0.0
        return int(rounded) if rounded.is_integer() and abs(rounded) < 1e15 else rounded
    if isinstance(value, (list, tuple, range)):
        return [_norm(v) for v in value]
    if isinstance(value, (set, frozenset)):
        return {"set": sorted((_canon(v) for v in value))}
    if isinstance(value, dict):
        return {"dict": sorted([_canon(k), _norm(v)] for k, v in value.items())}
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        return {"dataclass": type(value).__name__,
                "fields": {f.name: _norm(getattr(value, f.name)) for f in dataclasses.fields(value)}}
    if isinstance(value, bytes):
        return {"bytes": value.hex()}
    return {"repr": repr(value)}


def _canon(value) -> str:
    return json.dumps(_norm(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def fingerprint(module: str, key: str, value) -> str:
    payload = f"{SALT}|{module}|{key}|{_canon(value)}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _current_test() -> tuple[str, str]:
    current = os.environ.get("PYTEST_CURRENT_TEST", "")
    path, _, rest = current.partition("::")
    test_name = rest.rsplit(" (", 1)[0]
    module = Path(path).stem.removeprefix("test_")
    return module, test_name


def _answer_key(module: str) -> dict[str, str]:
    if module not in _keys:
        path = ANSWERS_DIR / f"{module}.json"
        _keys[module] = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    return _keys[module]


def _contains_blank(value, depth: int = 0) -> bool:
    """True if a ___ placeholder (from a notebook workbook) is in the value."""
    if type(value).__name__ == "_Blank":
        return True
    if depth < 4 and isinstance(value, (list, tuple, set, frozenset)):
        return any(_contains_blank(v, depth + 1) for v in value)
    if depth < 4 and isinstance(value, dict):
        return any(_contains_blank(k, depth + 1) or _contains_blank(v, depth + 1) for k, v in value.items())
    return False


def check(actual, hint: str = "") -> None:
    """Pass if `actual` is the correct value for this point of the test."""
    __tracebackhide__ = True  # show the learner's test line, not grader internals
    if _contains_blank(actual):
        raise NotImplementedError("fill in the ___ blanks")
    module, test_name = _current_test()
    _counters[test_name] += 1
    key = f"{test_name}#{_counters[test_name]}"
    digest = fingerprint(module, key, actual)
    if RECORDING:
        _recorded[module][key] = digest
        return
    expected = _answer_key(module).get(key)
    if expected is None:
        raise AssertionError(f"No answer key for {module}:{key}. A maintainer needs to rebuild "
                             "the keys (see practice/README.md, 'For maintainers').")
    if digest != expected:
        caller = inspect.stack()[1]
        line = (caller.code_context or ["?"])[0].strip()
        inputs = {k: v for k, v in caller.frame.f_locals.items()
                  if not k.startswith("_") and k not in {"m", "self"} and not inspect.ismodule(v)
                  and not callable(v) and len(repr(v)) < 200}
        message = [f"Not correct yet: {line}", f"  your result: {actual!r}"]
        if inputs:
            message.append("  test inputs: " + ", ".join(f"{k}={v!r}" for k, v in inputs.items()))
        if hint and SHOW_HINTS:
            message.append(f"  hint: {hint}")
        message.append("  (The correct answer is hidden. Re-read the docstring and try a small example by hand.)")
        raise AssertionError("\n".join(message))


def write_recorded() -> list[Path]:
    """Write the answer keys captured while RECORDING. Returns the files written."""
    ANSWERS_DIR.mkdir(exist_ok=True)
    written = []
    for module, keys in sorted(_recorded.items()):
        path = ANSWERS_DIR / f"{module}.json"
        path.write_text(json.dumps(dict(sorted(keys.items())), indent=1) + "\n", encoding="utf-8")
        written.append(path)
    return written
