# Level 1 — Python Basics

A complete beginner-friendly Python course with **18 lesson notebooks** that teach a little and test it straight away: **200 fill-in exercises** from easy to hard and **72 auto-graded challenges**, plus **3 mini-projects**. No prior programming experience is expected.

## Learning outcomes

By the end you should be able to explain Python's main types, write control flow, choose between lists/tuples/sets/dictionaries, design functions, handle errors, read/write files and CSV, debug small programs, and solve everyday algorithmic tasks.

## Detailed lesson index

| # | Notebook |
|---:|---|
| 1 | [00 python introduction](notebooks/00_python_introduction.ipynb) |
| 2 | [01 variables and data types](notebooks/01_variables_and_data_types.ipynb) |
| 3 | [02 operators](notebooks/02_operators.ipynb) |
| 4 | [03 strings](notebooks/03_strings.ipynb) |
| 5 | [04 input and output](notebooks/04_input_and_output.ipynb) |
| 6 | [05 conditional statements](notebooks/05_conditional_statements.ipynb) |
| 7 | [06 loops](notebooks/06_loops.ipynb) |
| 8 | [07 lists](notebooks/07_lists.ipynb) |
| 9 | [08 tuples and sets](notebooks/08_tuples_and_sets.ipynb) |
| 10 | [09 dictionaries](notebooks/09_dictionaries.ipynb) |
| 11 | [10 functions](notebooks/10_functions.ipynb) |
| 12 | [11 scope and builtins](notebooks/11_scope_and_builtins.ipynb) |
| 13 | [12 exception handling](notebooks/12_exception_handling.ipynb) |
| 14 | [13 file handling](notebooks/13_file_handling.ipynb) |
| 15 | [14 modules and standard library](notebooks/14_modules_and_standard_library.ipynb) |
| 16 | [15 debugging basics](notebooks/15_debugging_basics.ipynb) |
| 17 | [16 basic problem solving](notebooks/16_basic_problem_solving.ipynb) |
| 18 | [17 python basics review](notebooks/17_python_basics_review.ipynb) |

### Units and milestones

| Unit | Lessons | Checkpoint |
|---|---|---|
| Getting Started | 00–04 | Write a formatted mini-profile and numeric converter |
| Decisions and Repetition | 05–06 | Solve condition and loop exercises |
| Collections | 07–09 | Implement a small in-memory catalog |
| Reusable Code | 10–11 | Test reusable functions without globals |
| Robust Programs | 12–14 | Read, validate, and write CSV |
| Program Quality | 15–17 | Debug and explain a small integrated application |

## Practice packs

The challenges live inside the lessons that teach their topic (lessons 01–14). Each one
is a function you finish and `check('name')` grades with the tests in
[`practice/`](../practice/), the same tests used to verify an achievement claim.

Each pack has an auto-graded module in [`practice/`](../practice/README.md). The tests tell you whether your answer is correct without showing the answer.

## Projects

1. [Calculator](projects/01_calculator.ipynb) — functions, input parsing, operators, and error handling
2. [Number Guessing Game](projects/02_number_guessing_game.ipynb) — random, conditions, loops, replay
3. [Student Grade Manager](projects/03_student_grade_manager.ipynb) — dictionaries, lists, validation, CSV persistence

## Suggested study plan (6 weeks, flexible)

| Week | Work |
|---|---|
| 1 | Lessons 00–04, fundamentals practice |
| 2 | Lessons 05–06, control flow practice |
| 3 | Lessons 07–09, data structures practice |
| 4 | Lessons 10–12, calculator and number guessing projects |
| 5 | Lessons 13–16, functions-and-files practice |
| 6 | Grade manager project, lesson 17, full review |

**Completion standard:** You can complete at least 80% of the practice questions without peeking, explain the programs you wrote, and run all three projects without exceptions from a fresh kernel. Use `python -m pytest practice -k basics` to see your progress.

## Troubleshooting

- If a variable is unexpectedly undefined, run cells in order or restart the kernel.
- If `input()` seems to freeze execution, the notebook may be waiting for an answer; the sample notebooks comment out optional interactive calls.
- If files are missing, print `Path.cwd()` and check the relative path.
- If a package cannot be imported, confirm the notebook kernel is using the environment where you installed it.

## Next level

Read the [Intermediate roadmap](../intermediate/README.md) after completing the Basics capstone.

## Worked examples and quizzes

- [Worked examples](worked_examples/01_worked_examples.ipynb): six problems solved step by step (plan → code → why → common mistake → your turn).
- Every lesson ends with a **Quick quiz** of three questions. Answers are hidden but checked when you run the cell.
