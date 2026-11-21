# Python Learning Notebooks 🐍

A free, hands-on Python course from Basics through Advanced. Start with short explanations, examples and guided checks. Later lessons ask you to implement complete components, diagnose failures and write regression tests. Each lesson includes a build assessed from your saved code. Engineering tickets and projects ask you to deliver and explain changes to working software.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/SwarmLadder/python-notebook)
[![Launch Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/SwarmLadder/python-notebook/main?urlpath=lab/tree/basics/notebooks/00_python_introduction.ipynb)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SwarmLadder/python-notebook/blob/main/basics/notebooks/00_python_introduction.ipynb)

**No install needed:** Codespaces gives you everything, including the auto-graded practice. Binder and Colab run the notebooks in your browser.

| Level | Lessons (each with a quiz) | Worked examples | Named practice checks | Practice tests | Projects |
|---|---:|---:|---:|---:|---:|
| [Basics](basics/README.md) | 18 | 6 | 72 | 231 | 3 |
| [Intermediate](intermediate/README.md) | 20 | 6 | 71 | 102 | 3 + CLI package |
| [Advanced](advanced/README.md) | 20 | 6 | 57 | 95 | 3 + CLI package |

## Start on your computer

Use Python **3.11 or 3.13**, the versions tested by this repository's CI matrix. Other versions may work but are not currently part of automated validation.

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
3. **Practice, implement and check.** Use short questions to learn the mechanics. In later sections, implement a function from its contract or repair a component and write a regression test. Run the independent build check on your saved code. Engineering submissions have their own acceptance criteria for review.
4. **Study the worked examples** (`<level>/worked_examples/`). They show how a solution is planned, written and tested.
5. **Solve the challenges** in each lesson. For guided tasks, fill in each `___`. For an independent build, implement the contract and add a boundary test. Run the check after your code. ✅ means move on. ❌ shows your result and the test's input, never the answer. Guided practice unlocks increasingly specific hints. Saved independent builds have a separate [mastery check](curriculum/MASTERY.md).
6. **Prefer a terminal?** The achievement-track practice modules are in `practice/exercises/`; check them with `python -m pytest practice -k basics_01`. See [practice/README.md](practice/README.md).
7. **Build the projects** and take the level's assessment before moving up.

Each lesson ends with a **Next:** link. Restart the kernel and run all cells once you finish a lesson.

## Get your name on the course

There are two tracks, both checked automatically (see [RECOGNITION.md](RECOGNITION.md)):

- **Contributors:** improve the course. A merged PR adds you to [CONTRIBUTORS.md](CONTRIBUTORS.md).
- **Achievers:** pass every challenge of a level. A verified claim adds you to [ACHIEVEMENTS.md](ACHIEVEMENTS.md).

## For contributors and teachers

- `python -m pytest` runs every check: each notebook from a fresh kernel, the docs links, the data files, the project packages and the practice tests.
- See [CONTRIBUTING.md](CONTRIBUTING.md). Questions, typo reports and translations are welcome.
- The [coverage audit](curriculum/AUDIT.md) and [concept map](curriculum/concepts.json) connect lessons to prerequisites, reused skills and independent work.
- Using this course in a class? It's free to use and adapt, with credit (see License).

## License

The lesson text and notebooks are under [CC BY 4.0](LICENSE-CONTENT.md). The code (examples, practice, tests, tools) is under the [MIT License](LICENSE).
