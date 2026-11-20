"""The first code cell of every notebook: makes the course files available on Google Colab.

Colab (and similar services) open a single .ipynb without the rest of the repository, so
helpers like lesson.py, quiz.py and check.py, the data files and practice/ are missing.
This cell clones the course once and moves into the notebook's own folder. In a normal
checkout `../README.md` exists, so it does nothing.
"""
REPO = "https://github.com/SwarmLadder/python-notebook"
CELL_ID = "colab-setup"


def setup_code(level: str, folder: str) -> str:
    return f'''# Setup: run this first. On Google Colab (or anywhere the course files are missing) it
# downloads the course and moves into this notebook's folder. Elsewhere it does nothing.
import os, sys
if not os.path.exists("../README.md"):
    course = os.path.join(os.path.expanduser("~"), "python-notebook")
    if not os.path.isdir(course):
        os.system(f"git clone -q --depth 1 {REPO} {{course}}")
    os.chdir(os.path.join(course, "{level}", "{folder}"))
    sys.path.insert(0, os.getcwd())'''


def setup_cell(level: str, folder: str) -> dict:
    lines = setup_code(level, folder).split("\n")
    return {"cell_type": "code", "execution_count": None, "id": CELL_ID, "metadata": {}, "outputs": [],
            "source": [line + "\n" for line in lines[:-1]] + [lines[-1]]}
