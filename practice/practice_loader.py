"""Load a practice module: your work in practice/exercises/, or (for maintainers)
the private reference solutions passed with --record-answers=DIR."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

HERE = Path(__file__).resolve().parent
SOURCE_DIR = HERE / "exercises"


def load(name: str) -> ModuleType:
    path = SOURCE_DIR / f"{name}.py"
    module_name = f"practice_{abs(hash(str(SOURCE_DIR)))}_{name}"
    if module_name in sys.modules:
        return sys.modules[module_name]
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module  # needed so dataclasses can resolve the module
    spec.loader.exec_module(module)
    return module


def module_for(test_file: str) -> ModuleType:
    """Return the practice module graded by a test file named test_<module>.py."""
    return load(Path(test_file).stem.removeprefix("test_"))
