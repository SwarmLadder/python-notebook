"""Exercise representative notebooks in genuine, isolated IPython kernels.

The fast notebook_runner uses exec(), not the interactive Jupyter protocol.
"""
from __future__ import annotations

import pytest

from notebook_runner import ROOT, cell_source, load

jupyter_client = pytest.importorskip("jupyter_client")

LESSONS = (
    "basics/notebooks/16_basic_problem_solving.ipynb",
    "intermediate/notebooks/09_functional_tools_and_itertools.ipynb",
    "advanced/notebooks/19_advanced_review_capstone.ipynb",
)


def run_cell(client, source: str) -> str:
    msg_id = client.execute(source, store_history=False)
    output = []
    while True:
        event = client.get_iopub_msg(timeout=15)
        if event.get("parent_header", {}).get("msg_id") != msg_id:
            continue
        kind = event["msg_type"]
        payload = event["content"]
        if kind == "stream":
            output.append(payload["text"])
        elif kind == "error":
            raise AssertionError(
                f"Kernel raised {payload['ename']}: {payload['evalue']}\n"
                + "\n".join(payload.get("traceback", []))
            )
        elif kind == "status" and payload.get("execution_state") == "idle":
            return "".join(output)


@pytest.mark.parametrize("name", LESSONS)
def test_representative_lesson_in_real_jupyter_kernel(name):
    path = ROOT / name
    cells = {cell["id"]: cell_source(cell) for cell in load(path)["cells"]}
    km = jupyter_client.KernelManager(kernel_name="python3")
    km.start_kernel(cwd=str(path.parent))
    client = km.client()
    client.start_channels()
    try:
        client.wait_for_ready(timeout=20)
        for step in ("colab-setup", "lesson-setup", "demo-1"):
            run_cell(client, cells[step])
        if name.startswith("basics/"):
            code = cells["ex-2"]
            untouched = run_cell(client, code)
            assert "Not attempted" in untouched, untouched
            correct = run_cell(client, code.replace("    ___", "    running.append(total)"))
            assert "correct" in correct and "Passed" in correct, correct
            incorrect = run_cell(client, code.replace("    ___", "    running.append(0)"))
            assert "Needs improvement" in incorrect, incorrect
            assert "False" in run_cell(client, "print(2 in check.passed)")
        else:
            pending = run_cell(client, cells["ex-1"])
            assert "Not attempted" in pending, pending
    finally:
        client.stop_channels()
        km.shutdown_kernel(now=True)
