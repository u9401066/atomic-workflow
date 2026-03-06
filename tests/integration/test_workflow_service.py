from __future__ import annotations

from pathlib import Path

from atomic_workflow.services.workflow_service import WorkflowService


def test_service_lists_phase_letters_from_repository() -> None:
    workflows_dir = Path(__file__).resolve().parents[2] / "workflows"
    service = WorkflowService.from_root(workflows_dir)

    assert service.list_phases("anesthesia") == list("ABCDEFGHIJKL")


def test_service_returns_resolved_step_for_elective_variant() -> None:
    workflows_dir = Path(__file__).resolve().parents[2] / "workflows"
    service = WorkflowService.from_root(workflows_dir)

    step = service.get_resolved_step("anesthesia", "A-01")

    assert step.resolved_step_key == "anesthesia:elective:A-01"
    assert step.origin == "baseline"
    assert step.variant == "elective"
    assert step.node_type == "task"


def test_service_returns_variant_only_and_modified_steps_for_emergency() -> None:
    workflows_dir = Path(__file__).resolve().parents[2] / "workflows"
    service = WorkflowService.from_root(workflows_dir)

    phase_b_steps = service.list_steps("anesthesia", phase="B", variant="emergency")
    modified_step = service.get_resolved_step("anesthesia", "A-01", variant="emergency")

    assert any(step.step_id == "B-E01" and step.origin == "variant_only" for step in phase_b_steps)
    assert all(step.step_id != "B-01" for step in phase_b_steps)
    assert modified_step.origin == "modified"
    assert modified_step.variant == "emergency"
    assert modified_step.items[0].text == "**接案方式**："