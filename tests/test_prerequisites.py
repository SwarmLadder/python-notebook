"""Keep the first Basics independent builds within taught prerequisites."""
import pytest
from notebook_runner import ROOT, load, cell_source


@pytest.mark.parametrize("number", [1, 2, 3, 5, 7, 8, 9])
def test_function_syntax_is_scaffolded_before_lesson_ten(number):
    notebook = next((ROOT / "basics" / "notebooks").glob(f"{number:02}_*.ipynb"))
    cells = load(notebook)["cells"]
    index = next(i for i, cell in enumerate(cells) if cell.get("id") == "independent-build")
    assert "Prerequisite bridge" in cell_source(cells[index])
    body = cell_source(cells[index + 1])
    assert "return result" in body
    assert "import " not in body


def test_file_build_has_path_import_before_function_header():
    path = ROOT / "basics/notebooks/13_file_handling.ipynb"
    cells = load(path)["cells"]
    index = next(i for i, cell in enumerate(cells) if cell.get("id") == "independent-build")
    earlier = "\n".join(cell_source(c) for c in cells[:index] if c["cell_type"] == "code")
    assert "from pathlib import Path" in earlier
    assert "path: Path" in cell_source(cells[index + 1])


def test_loop_build_provides_function_header_and_return_explanation():
    path = ROOT / "basics/notebooks/06_loops.ipynb"
    cells = load(path)["cells"]
    index = next(i for i, cell in enumerate(cells) if cell.get("id") == "independent-build")
    assert "return" in cell_source(cells[index])
    assert cell_source(cells[index + 1]).startswith("# The function header is provided")


def test_receipt_build_is_input_dependent_and_scaffolded():
    path = ROOT / "basics/notebooks/04_input_and_output.ipynb"
    cells = load(path)["cells"]
    index = next(i for i, cell in enumerate(cells) if cell.get("id") == "independent-build")
    source = cell_source(cells[index + 1])
    assert source.startswith("# Function syntax is supplied")
    assert "def receipt(item, units):" in source and "return result" in source
    assert "import " not in source
