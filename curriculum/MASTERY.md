# Independent mastery

Save your independent build in its original lesson cell. From the checkout, run one lesson or a whole level.

```sh
python tools/assess_build.py b06
python tools/assess_build.py intermediate --json
```

The command starts a fresh Python process per lesson, runs the supplied setup and explicitly declared prerequisites, then grades the saved work in that isolated context. A missing definition, failed or skipped check, exception or timeout yields an incomplete attempt and a nonzero exit code. The receipt exercise also gets a different order on replay. Each JSON record names the concept and build and reports the current result. Course practice tests require pytest.

Use the guided exercises for hints. The assessment reruns the behavioral checks without progressive hints. A passing report records demonstrated behavior on those cases. Ask the learner to reproduce a boundary case, explain a decision and handle a changed requirement in the project review. Local reports do not establish authorship or record assistance received outside the attempt.

The [concept map](concepts.json) identifies the new skill and earlier concepts reused. Selected delayed revisions also list `assessed_reuse`, the earlier concepts exercised in the build or its review evidence. Run `python tools/course_stats.py` for inventory. Named practice checks and independent builds overlap. The [achievement process](../RECOGNITION.md) uses the existing practice modules.
