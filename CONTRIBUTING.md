# Contributing

Thanks for helping more people learn Python! Small fixes are as welcome as new lessons.

## Ways to help

- **Report a confusing explanation or a bug.** Open an issue and say which notebook, which cell, and what you expected.
- **Fix typos or unclear wording.** Shorter and clearer beats longer.
- **Translate** a lesson. Put it next to the original with a language suffix, e.g. `06_loops.es.ipynb`.
- **Add practice.** See "Practice tests" below.

## Style

- One idea per section: a short explanation, a runnable example, and one question for the reader.
- Plain words, short sentences, no filler. Explain *why*, not just *what*.
- Examples use only the standard library and run offline, and the notebook works with **Restart & Run All**.
- Clear outputs before committing (Jupyter: *Edit → Clear Outputs of All Cells*).

## Before opening a pull request

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
```

This runs every notebook from a fresh kernel. It also checks titles, cleared outputs, **Next** links, Markdown links, data files, the project packages and the practice tests.

## Practice tests

Practice answers are hidden. Tests call `check(value)`, and the repo stores only a hash of each correct value. The reference solutions live in a private folder kept by the maintainers.

To propose a new exercise:
1. Add the function signature and a docstring (with an example and a hint) to `practice/exercises/<module>.py`. Its body must be `raise NotImplementedError(...)`.
2. Add tests that use `check(...)`, or plain `assert`s for rules that don't reveal the answer.
3. Put your reference implementation in the PR description or a gist instead of the repo. A maintainer adds it to the private solutions and rebuilds the answer keys (see [practice/README.md](practice/README.md#for-maintainers)).

## License

By contributing you agree that text and notebooks are licensed under CC BY 4.0 and code under MIT (see [LICENSE-CONTENT.md](LICENSE-CONTENT.md) and [LICENSE](LICENSE)).
