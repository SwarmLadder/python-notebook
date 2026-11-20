# Python Learning Notebooks 🐍

A practical, structured Python learning course organized into **Basics → Intermediate → Advanced**. The repository emphasizes explanations, runnable code, independent practice, and projects rather than isolated syntax snippets.

## Choose your path

| Level | Status | Focus |
| --- | --- | --- |
| [Basics](basics/README.md) | **Detailed notebooks ready** | Syntax, types, branching, loops, data structures, functions, errors, files, debugging, mini-projects |
| [Intermediate](intermediate/README.md) | **Detailed notebooks ready** | 20 lessons, 80 extra problems, 24 worked solutions, 3 projects, installable SQLite CLI |
| [Advanced](advanced/README.md) | Curriculum roadmap | Concurrency, asyncio, internals, profiling, architecture, production-quality Python |

## Quick start

1. Install Python 3.10 or newer.
2. Clone this repository and open a terminal in its root directory.
3. Create a virtual environment: `python -m venv .venv`.
4. Activate it: macOS/Linux: `source .venv/bin/activate`; Windows PowerShell: `.venv\Scripts\Activate.ps1`.
5. Run `python -m pip install -r requirements.txt`.
6. Launch with `jupyter lab` and open `basics/notebooks/00_python_introduction.ipynb`.

You can also read rendered .ipynb files directly on GitHub, but running their cells requires Jupyter or a compatible environment.

## Course design

- **18** carefully ordered beginner lessons with explanatory Markdown, runnable examples, exercises, and self-check prompts
- **4** practice workbooks containing **60** additional problems
- **4** answer workbooks with worked reference approaches
- **3** Basics mini-projects and **3** Intermediate portfolio projects (including an installable CLI)
- Reproducible examples: no network, secret keys, paid services, or third-party libraries required beyond Jupyter itself

## Intermediate course

After Basics, open [the Intermediate syllabus](intermediate/README.md) to study 20 guided notebooks, 80 additional exercise challenges, 24 worked examples, offline APIs, testing, SQLite, and packaging. The [final assessment](intermediate/ASSESSMENT.md) includes a 100-point rubric. The Advanced track remains a roadmap.

## Recommended learning workflow

Read one lesson at a time. Predict before running examples, then change one input and explain the result. Solve the lesson exercises, complete a matching practice pack, and only then read the worked solutions. Complete the three projects and the final assessment before moving to Intermediate.

## Contributing

Contributions and corrections are welcome. Keep explanations beginner-friendly, code cells executable from a fresh kernel, and dependencies minimal.

See [the Basics syllabus](basics/README.md) and [the Intermediate syllabus](intermediate/README.md) for ordered lesson links, practice, milestones, and assessments.
