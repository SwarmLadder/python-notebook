"""Checks for the non-notebook files: docs links, data fixtures, scripts."""
import csv
import json
import re
import subprocess
import sys

import pytest

from notebook_runner import LEVELS, ROOT

MARKDOWN = sorted(p for p in ROOT.rglob("*.md") if ".git" not in p.parts and ".pytest_cache" not in p.parts)
LINK = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)")


@pytest.mark.parametrize("path", MARKDOWN, ids=[p.relative_to(ROOT).as_posix() for p in MARKDOWN])
def test_markdown_relative_links_resolve(path):
    broken = [target for target in LINK.findall(path.read_text(encoding="utf-8"))
              if not re.match(r"[a-z]+:", target) and not (path.parent / target).exists()]
    assert not broken, f"broken links: {broken}"


DATA = sorted(p for level in LEVELS for p in (ROOT / level / "data").glob("*") if p.suffix in {".json", ".csv"})


@pytest.mark.parametrize("path", DATA, ids=[p.relative_to(ROOT).as_posix() for p in DATA])
def test_data_fixtures_parse(path):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        json.loads(text)
    else:
        rows = list(csv.DictReader(text.splitlines()))
        assert rows, "CSV fixture should have at least one data row"
        assert all(None not in row for row in rows), "row has more fields than the header"


PY_FILES = sorted(p for p in ROOT.rglob("*.py") if ".git" not in p.parts and "__pycache__" not in p.parts)


@pytest.mark.parametrize("path", PY_FILES, ids=[p.relative_to(ROOT).as_posix() for p in PY_FILES])
def test_python_file_compiles(path):
    compile(path.read_text(encoding="utf-8"), str(path), "exec")


SCRIPTS = ["tools/validate_notebooks.py", "advanced/examples/process_pool_demo.py"]


@pytest.mark.parametrize("script", SCRIPTS)
def test_script_runs(script):
    result = subprocess.run([sys.executable, script], cwd=ROOT, capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stdout + result.stderr
