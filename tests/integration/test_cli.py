from __future__ import annotations

import json
import subprocess
from pathlib import Path


def test_cli_get_phase_graph_outputs_json() -> None:
    root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [
            "uv",
            "run",
            "python",
            "-m",
            "atomic_workflow.cli",
            "get-phase-graph",
            "--domain",
            "anesthesia",
            "--phase",
            "A",
        ],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )

    payload = json.loads(result.stdout)

    assert payload["meta"]["phase"] == "A"
    assert payload["nodes"]