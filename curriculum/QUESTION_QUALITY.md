# Student question quality standard

A question is ready when it is **correct, clear, concise, meaningful,
prerequisite-safe and testable**. The problem—not hidden syntax,
contradictory examples, or tooling—is what a student should have to solve.

## Small guided exercises

State the action, the actual input and the observable result. Explain an
unfamiliar term in one sentence. Avoid a long story or many artificial
headings. Example:

> **Exercise 2.** Running totals — A running total includes everything
> processed so far. For `[1, 2, 3, 4]`, build `[1, 3, 6, 10]`.
> Fill the line in the loop so the updated total is recorded each time.

The prompt must match the code. A deliberately *different illustrative*
example must be labeled as such. Do not insert untaught imports or library
requirements in a learner-written exercise; supply setup code until that
concept is explicitly taught.

## Independent builds

Describe the callable or artifact contract, normal behavior, ordering,
empty/boundary behavior, error behavior if relevant, and input ownership.
Include a discriminating example, but leave implementation strategy open.
Prefer a real Order Desk request, regression or review ticket over a
contrived story. At Advanced level make relevant invariants, performance
constraints and failure handling explicit.

Guided hints should progress from investigation, to a previously taught
concept, to a specific nudge. Withhold these from independent assessment;
hint-assisted completion is not independent mastery evidence.

## Checks and evidence

- Missing work or unresolved `___` is **Not attempted**, not incorrect.
- A completed wrong answer is **Needs improvement**, with a useful
  diagnostic. A correct checked answer is **Passed**.
- Every prompt has a corresponding code cell and assessment. Distinguish
  text examples from literal input fixtures.
- Check representative normal, boundary, empty and required invalid
  cases; preserve inputs where the contract requires it.
- Use behaviorally meaningful tests that reject plausible mistakes and
  permit alternative correct implementations. Keep private reference
  solutions outside this public repository.
- A passing public exercise check is *practice evidence*. A separately
  checked saved build is *local independent-build evidence*, not proof of
  authorship. Engineering qualification additionally requires a tested
  project change and design review.
- When an earlier concept is marked `assessed_reuse`, demonstrate the
  later observable task requiring it; otherwise list it as possible
  `reused_concepts` or remove the claim.

## Editorial review

Before publishing, read the rendered prompt next to its actual starter
code. Run the empty submission, a valid submission and a plausible
wrong submission. Confirm the fingerprints, feedback, indentation,
examples and links in both a clean Jupyter kernel and the Lab browser.
Structural tests can guard consistency, but do not replace an educator's
review of clarity or whether the exercise teaches the intended skill.
