"""Recognition tooling: claim validation and the ACHIEVEMENTS / CONTRIBUTORS file updates."""
import shutil
import subprocess
import sys

import pytest

from notebook_runner import ROOT

sys.path.insert(0, str(ROOT / "tools"))
import check_claim  # noqa: E402
import recognition  # noqa: E402


@pytest.fixture
def files(tmp_path, monkeypatch):
    for name in ("ACHIEVEMENTS.md", "CONTRIBUTORS.md"):
        shutil.copy(ROOT / name, tmp_path / name)
    monkeypatch.setattr(recognition, "ACHIEVEMENTS", tmp_path / "ACHIEVEMENTS.md")
    monkeypatch.setattr(recognition, "CONTRIBUTORS", tmp_path / "CONTRIBUTORS.md")
    return tmp_path


def test_achievement_is_added_once_per_level(files):
    assert recognition.add_achievement("ada-l", "basics", "Ada | L", "https://x/pr/9", "2026-11-20")
    assert not recognition.add_achievement("ada-l", "basics", "Ada", "https://x/pr/10")
    assert recognition.add_achievement("ada-l", "advanced", "", "https://x/pr/11")
    text = (files / "ACHIEVEMENTS.md").read_text()
    basics = text.split("## 🥉 Basics")[1].split("\n## ")[0]
    assert "[@ada-l](https://github.com/ada-l) | Ada L | 2026-11-20" in basics
    assert "Be the first" not in basics and "Be the first" in text  # intermediate is still empty


def test_contributor_is_added_once(files):
    assert recognition.add_contributor("bob", "https://x/pr/3", "Fix typo [lesson 6]")
    assert not recognition.add_contributor("bob", "https://x/pr/4", "again")
    text = (files / "CONTRIBUTORS.md").read_text()
    assert text.count("@bob") == 1 and "Your name here" not in text


@pytest.mark.parametrize("login", ["../../etc", "a b", "x" * 50, ""])
def test_bad_logins_are_refused(files, login):
    with pytest.raises(ValueError):
        recognition.add_contributor(login, "u", "t")


def test_claim_may_only_touch_exercises_and_own_claim():
    ok = ["practice/exercises/basics_01_fundamentals.py", "basics/exercises/02_control_flow_exercises.ipynb",
          "achievements/claims/ada.md"]
    assert check_claim.validate_files(ok, "ada") == "achievements/claims/ada.md"
    for files in (ok + ["practice/grader.py"], ok + [".github/workflows/verify-achievement.yml"],
                  ["achievements/claims/eve.md"], ["practice/exercises/x.py"]):
        with pytest.raises(check_claim.ClaimError):
            check_claim.validate_files(files, "ada")


def test_claim_file_format():
    assert check_claim.parse_claim("level: Basics\nname: Ada Lovelace") == ("basics", "Ada Lovelace")
    assert check_claim.parse_claim("# my claim\nlevel: advanced  # yay") == ("advanced", "")
    for bad in ("level: expert", "name: Ada", "level: basics\nname: <script>alert(1)</script>"):
        with pytest.raises(check_claim.ClaimError):
            check_claim.parse_claim(bad)


def test_verify_level_rejects_blank_exercises():
    result = subprocess.run([sys.executable, "tools/verify_level.py", "basics"], cwd=ROOT,
                            capture_output=True, text=True, timeout=600)
    assert result.returncode == 1
    assert "not complete yet" in result.stdout
