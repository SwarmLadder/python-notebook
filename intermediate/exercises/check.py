"""Lets the workbook notebooks in this folder use the auto-graded practice tests."""
import sys
from pathlib import Path

_practice = Path(__file__).resolve().parents[2] / "practice"
if str(_practice) not in sys.path:
    sys.path.insert(0, str(_practice))

from notebook_check import Checker, ___  # noqa: E402,F401
