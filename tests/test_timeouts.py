"""The repo-wide time limit turns an infinite loop into a clear failure instead of a hang."""
import os
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

from notebook_runner import ROOT


def test_infinite_loop_fails_with_advice():
    with tempfile.TemporaryDirectory(dir=ROOT, prefix="_timeout_check_") as folder:
        test_file = Path(folder) / "test_loop.py"
        test_file.write_text(textwrap.dedent("""
            def test_forever():
                n = 1
                while n > 0:
                    n += 1
        """))
        env = {**os.environ, "PYTEST_TIMEOUT": "1"}
        result = subprocess.run([sys.executable, "-m", "pytest", str(test_file), "-q", "-p", "no:cacheprovider"],
                                cwd=ROOT, capture_output=True, text=True, timeout=60, env=env)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "infinite loop" in result.stdout
