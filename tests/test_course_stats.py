"""Course counts are generated from the actual notebooks, not stale manual claims."""
import subprocess
import sys

from notebook_runner import ROOT


def test_documented_course_statistics_are_current():
    run = subprocess.run([sys.executable, "tools/course_stats.py", "--check"],
                         cwd=ROOT, text=True, capture_output=True, timeout=30)
    assert run.returncode == 0, run.stdout + run.stderr
