from __future__ import annotations

from pathlib import Path

import pytest

from atomic_workflow.domain.errors import DuplicateStepError, StepNotFoundError
from atomic_workflow.domain.models import BaselineStep
from atomic_workflow.repository.step_index import StepIndex


def _make_step(step_id: str, phase: str, sequence: int) -> BaselineStep:
    return BaselineStep(
        baseline_step_id=step_id,
        domain="anesthesia",
        phase=phase,
        sequence=sequence,
        title=f"Step {step_id}",
        roles=[],
        items=[],
        warnings=[],
        tags=[],
        source_file=f"phase-{phase.lower()}.md",
    )


def test_step_index_tracks_phase_files_and_step_locations() -> None:
    index = StepIndex.from_files(
        "anesthesia",
        [
            (Path("phase-a-preop.md"), [_make_step("A-01", "A", 1)]),
            (Path("phase-b-ward-prep.md"), [_make_step("B-01", "B", 1)]),
        ],
    )

    assert index.list_phases() == ["A", "B"]
    assert index.get_step_location("A-01").source_file == Path("phase-a-preop.md")
    assert index.has_step("B-01") is True


def test_step_index_raises_for_duplicate_step_id() -> None:
    with pytest.raises(DuplicateStepError):
        StepIndex.from_files(
            "anesthesia",
            [
                (Path("phase-a.md"), [_make_step("A-01", "A", 1)]),
                (Path("phase-a-copy.md"), [_make_step("A-01", "A", 1)]),
            ],
        )


def test_step_index_raises_for_missing_step() -> None:
    index = StepIndex.from_files(
        "anesthesia",
        [(Path("phase-a.md"), [_make_step("A-01", "A", 1)])],
    )

    with pytest.raises(StepNotFoundError):
        index.get_step_location("A-99")