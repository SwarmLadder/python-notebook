"""Select the saved code cells that define a reproducible exercise context."""
from __future__ import annotations


def selected_cells(notebook, target):
    """Return setup, transitive prerequisites and target exactly once, in order."""
    cells = notebook["cells"]
    positions = {cell["id"]: index for index, cell in enumerate(cells)}
    selected = set()

    def include(cell_id):
        cell = cells[positions[cell_id]]
        if cell_id in selected:
            return
        if cell["cell_type"] != "code":
            raise ValueError(f"{cell_id} is not executable")
        for dependency in cell.get("metadata", {}).get("requires_cells", []):
            if dependency not in positions or positions[dependency] >= positions[cell_id]:
                raise ValueError(f"{cell_id} requires an earlier code cell: {dependency}")
            include(dependency)
        selected.add(cell_id)

    for cell_id in ("colab-setup", "lesson-setup", target):
        include(cell_id)
    return [cell for cell in cells if cell["id"] in selected]
