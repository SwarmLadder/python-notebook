# Python Learning Notebooks 🐍

A practical, structured Python learning course organized into **Basics → Intermediate → Advanced**. The repository emphasizes explanations, runnable code, independent practice, and projects rather than isolated syntax snippets.

## Choose your path

| Level | Status | Focus |
| --- | --- | --- |
| [Basics](basics/README.md) | **Detailed notebooks ready** | Syntax, types, branching, loops, data structures, functions, errors, files, debugging, mini-projects |
| [Intermediate](intermediate/README.md) | **Detailed notebooks ready** | 20 lessons, 80 extra problems, 24 worked solutions, 3 projects, installable SQLite CLI |
| [Advanced](advanced/README.md) | **Detailed notebooks ready** | 20 lessons, 80 challenges, 24 worked solutions, 3 capstones and installable event processor CLI |

## Quick start

1. Install Python 3.11 or newer for **all three levels** (Basics and Intermediate also support Python 3.10).
2. Clone this repository and open a terminal in its root directory.
3. Create a virtual environment: `python -m venv .venv`.
4. Activate it: macOS/Linux: `source .venv/bin/activate`; Windows PowerShell: `.venv\Scripts\Activate.ps1`.
5. Run `python -m pip install -r requirements.txt`.
6. Launch with `jupyter lab` and open `basics/notebooks/00_python_introduction.ipynb`.

You can also read rendered .ipynb files directly on GitHub, but running their cells requires Jupyter or a compatible environment.

## Course design and learning materials

| Level | Guided lessons | Extra exercises | Reference solutions | Projects | Total notebooks |
|---|---:|---:|---:|---:|---:|
| Basics | 18 | 60 | Representative solutions | 3 | 29 |
| Intermediate | 20 | 80 | 24 | 3 | 31 |
| Advanced | 20 | 80 | 24 | 3 | 31 |
| **Total** | **58** | **220** | — | **9** | **91** |

Lessons include explanatory Markdown, runnable examples, exercises, and self-check prompts. Sample code uses the standard library, with Jupyter required to execute notebooks. Intermediate and Advanced also include installable example CLI packages and automated tests. Advanced uses Python 3.11+ for structured concurrency.

## Intermediate course

After Basics, open [the Intermediate syllabus](intermediate/README.md) to study 20 guided notebooks, 80 additional exercise challenges, 24 worked examples, offline APIs, testing, SQLite, and packaging. The [final assessment](intermediate/ASSESSMENT.md) includes a 100-point rubric. The Advanced track is also fully developed, with advanced concurrency, performance, security and production engineering notebooks.

## Advanced course

After Intermediate, follow [the Advanced syllabus](advanced/README.md) through 20 detailed notebooks, 80 independent exercises, 24 worked reference examples, and three portfolio capstones. The [final assessment](advanced/ASSESSMENT.md) includes a 100-point rubric and tests for concurrency, security, and transaction behavior.

## Recommended learning workflow

Read one lesson at a time. Predict before running examples, then change one input and explain the result. Solve the lesson exercises, complete a matching practice pack, and only then read the worked solutions. Complete each level's projects and final assessment before advancing to the next level.

## Contributing

Contributions and corrections are welcome. Keep explanations beginner-friendly, code cells executable from a fresh kernel, and dependencies minimal.

See the [Basics syllabus](basics/README.md), [Intermediate syllabus](intermediate/README.md), and [Advanced syllabus](advanced/README.md) for detailed lesson links, projects, and assessments.
