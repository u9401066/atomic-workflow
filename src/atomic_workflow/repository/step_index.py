from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from atomic_workflow.domain.errors import DuplicateStepError, StepNotFoundError
from atomic_workflow.domain.models import BaselineStep


@dataclass(frozen=True, slots=True)
class StepLocation:
    step_id: str
    domain: str
    phase: str
    source_file: Path
    order: int


class StepIndex:
    def __init__(self) -> None:
        self._by_step_id: dict[str, StepLocation] = {}
        self._phase_files: dict[str, Path] = {}

    @classmethod
    def from_files(
        cls,
        domain: str,
        file_steps: list[tuple[Path, list[BaselineStep]]],
    ) -> "StepIndex":
        index = cls()
        for file_path, steps in file_steps:
            if not steps:
                continue
            phase = steps[0].phase
            index._phase_files[phase] = file_path
            for order, step in enumerate(steps):
                if step.baseline_step_id in index._by_step_id:
                    raise DuplicateStepError(
                        f"Duplicate step ID detected: {step.baseline_step_id}"
                    )
                index._by_step_id[step.baseline_step_id] = StepLocation(
                    step_id=step.baseline_step_id,
                    domain=domain,
                    phase=step.phase,
                    source_file=file_path,
                    order=order,
                )
        return index

    def get_step_location(self, step_id: str) -> StepLocation:
        try:
            return self._by_step_id[step_id]
        except KeyError as exc:
            raise StepNotFoundError(f"Unknown step ID: {step_id}") from exc

    def has_step(self, step_id: str) -> bool:
        return step_id in self._by_step_id

    def list_phases(self) -> list[str]:
        return sorted(self._phase_files)

    def phase_file(self, phase: str) -> Path:
        return self._phase_files[phase]