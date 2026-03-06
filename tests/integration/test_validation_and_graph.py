from __future__ import annotations

from pathlib import Path

from atomic_workflow.services.workflow_service import WorkflowService


def test_validate_domain_returns_valid_report_for_current_corpus() -> None:
    workflows_dir = Path(__file__).resolve().parents[2] / "workflows"
    service = WorkflowService.from_root(workflows_dir)

    report = service.validate_domain("anesthesia")

    assert report.valid is True
    assert report.stats["errors"] == 0


def test_get_phase_graph_returns_reactflow_payload() -> None:
    workflows_dir = Path(__file__).resolve().parents[2] / "workflows"
    service = WorkflowService.from_root(workflows_dir)

    graph = service.get_phase_graph("anesthesia", "A", variant="emergency")

    assert graph["meta"]["phase"] == "A"
    assert graph["nodes"]
    assert graph["edges"]
    assert graph["nodes"][0]["data"]["variant"] == "emergency"