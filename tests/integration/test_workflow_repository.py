from __future__ import annotations

from pathlib import Path

from atomic_workflow.repository.workflow_repository import WorkflowRepository


def test_repository_lists_baseline_steps_from_real_corpus() -> None:
    workflows_dir = Path(__file__).resolve().parents[2] / "workflows"
    repository = WorkflowRepository(workflows_dir)

    steps = repository.list_baseline_steps("anesthesia", phase="A")

    assert len(steps) == 14
    assert steps[0].baseline_step_id == "A-01"
    assert steps[0].title == "接到麻醉照會單 / 術前門診排定"
    assert steps[-1].baseline_step_id == "A-14"


def test_repository_get_baseline_step_returns_step_with_links() -> None:
    workflows_dir = Path(__file__).resolve().parents[2] / "workflows"
    repository = WorkflowRepository(workflows_dir)

    step = repository.get_baseline_step("anesthesia", "A-02")

    assert step.prev_step_id == "A-01"
    assert step.next_step_id == "A-03"
    assert step.roles[0].role_code == "anesthesiologist"


def test_repository_lists_variant_operations_from_real_corpus() -> None:
    workflows_dir = Path(__file__).resolve().parents[2] / "workflows"
    repository = WorkflowRepository(workflows_dir)

    operations = repository.list_variant_operations("anesthesia", "emergency")

    assert operations[0].variant == "emergency"
    assert any(operation.variant_step_id == "B-E01" for operation in operations)
    assert any(operation.operation == "skip" for operation in operations)