"""Print course inventory from notebook cells and the curriculum map."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def inventory():
    rows = json.loads((ROOT / "curriculum/concepts.json").read_text())
    for level in ("basics", "intermediate", "advanced"):
        lessons = sorted((ROOT / level / "notebooks").glob("*.ipynb"))
        guided = named = 0
        for path in lessons:
            cells = json.loads(path.read_text())["cells"]
            for cell in cells:
                if cell["cell_type"] == "code":
                    code = "".join(cell["source"])
                    guided += bool(re.search(r"^check\(\d+,", code, re.MULTILINE))
                    named += bool(re.fullmatch(r"check\('\w+'\)", code.strip()))
        yield {"level": level, "lessons": len(lessons), "guided": guided,
               "named_practice_checks": named, "independent_builds": sum(
                   row["lesson"].startswith(level + "/") for row in rows),
               "projects": len(list((ROOT / level / "projects").glob("*.ipynb")))}


if __name__ == "__main__":
    print(json.dumps(list(inventory()), indent=2))
