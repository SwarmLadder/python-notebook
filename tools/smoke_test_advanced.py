#!/usr/bin/env python3
"""Run the advanced notebook execution smoke test."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tests"))
from notebook_runner import smoke_level


if __name__ == "__main__":
    smoke_level("advanced")
