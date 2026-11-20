# Python Learning Notebooks 🐍

A free, hands-on Python course: **Basics → Intermediate → Advanced**. You read short lessons, run the examples and write your own code. Auto-graded exercises tell you whether you're right without showing the answer.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/SwarmLadder/python-notebook)
[![Launch Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/SwarmLadder/python-notebook/main?urlpath=lab/tree/basics/notebooks/00_python_introduction.ipynb)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SwarmLadder/python-notebook/blob/main/basics/notebooks/00_python_introduction.ipynb)

**No install needed:** Codespaces gives you everything, including the auto-graded practice. Binder and Colab run the notebooks in your browser.

| Level | Lessons | Workbook problems | Auto-graded tests | Projects |
|---|---:|---:|---:|---:|
| [Basics](basics/README.md) | 18 | 60 | 231 | 3 |
| [Intermediate](intermediate/README.md) | 20 | 80 | 102 | 3 + CLI package |
| [Advanced](advanced/README.md) | 20 | 80 | 95 | 3 + CLI package |

## Start on your computer

You need Python 3.11+. Basics and Intermediate also work on 3.10.

```bash
git clone https://github.com/SwarmLadder/python-notebook.git
cd python-notebook
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
jupyter lab                      # open basics/notebooks/00_python_introduction.ipynb
```

## How to study

1. **Read a lesson** and predict each cell's output before you run it.
2. **Change one input** and explain what happened.
3. **Do the lesson exercises,** then the level's workbook.
4. **Check yourself** with the auto-graded module for that workbook:

   ```bash
   python -m pytest practice -k basics_01
   ```

   You see "correct" or "not correct yet" with your result and the test's inputs, never the answer. See [practice/README.md](practice/README.md).
5. **Build the projects** and take the level's assessment before moving up.

Each lesson ends with a **Next:** link. Restart the kernel and run all cells once you finish a lesson.

## For contributors and teachers

- `python -m pytest` runs every check: each notebook from a fresh kernel, the docs links, the data files, the project packages and the practice tests.
- See [CONTRIBUTING.md](CONTRIBUTING.md). Questions, typo reports and translations are welcome.
- Using this course in a class? It's free to use and adapt, with credit (see License).

## License

The lesson text and notebooks are under [CC BY 4.0](LICENSE-CONTENT.md). The code (examples, practice, tests, tools) is under the [MIT License](LICENSE).
