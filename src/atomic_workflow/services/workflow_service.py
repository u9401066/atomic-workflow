from __future__ import annotations

from pathlib import Path

from atomic_workflow.domain.models import BaselineStep, ResolvedStep, ValidationReport
from atomic_workflow.graph import WorkflowGraphGenerator
from atomic_workflow.repository.workflow_repository import WorkflowRepository
from atomic_workflow.resolver import VariantResolver
from atomic_workflow.validation import WorkflowValidator


class WorkflowService:
    def __init__(self, repository: WorkflowRepository) -> None:
        self._repository = repository
        self._resolver = VariantResolver()
        self._validator = WorkflowValidator(repository)
        self._graph_generator = WorkflowGraphGenerator()

    @classmethod
    def from_root(cls, workflows_dir: Path) -> "WorkflowService":
        return cls(WorkflowRepository(workflows_dir))

    def list_phases(self, domain: str) -> list[str]:
        return self._repository.list_phases(domain)

    def list_domains(self) -> list[str]:
        return self._repository.list_domains()

    def list_variants(self, domain: str) -> list[str]:
        return ["elective", *self._repository.list_variants(domain)]

    def get_baseline_step(self, domain: str, step_id: str) -> BaselineStep:
        return self._repository.get_baseline_step(domain, step_id)

    def list_steps(
        self,
        domain: str,
        *,
        phase: str | None = None,
        variant: str = "elective",
    ) -> list[ResolvedStep]:
        baseline_steps = self._repository.list_baseline_steps(domain, phase=phase)
        if variant == "elective":
            return [self._to_resolved_step(step) for step in baseline_steps]
        operations = self._repository.list_variant_operations(domain, variant)
        resolved = self._resolver.resolve(baseline_steps, operations, variant=variant)
        if phase is not None:
            return [step for step in resolved if step.phase == phase]
        return resolved

    def get_resolved_step(
        self,
        domain: str,
        step_id: str,
        *,
        variant: str = "elective",
    ) -> ResolvedStep:
        if variant == "elective":
            return self._to_resolved_step(self._repository.get_baseline_step(domain, step_id))
        for resolved_step in self.list_steps(domain, variant=variant):
            if resolved_step.step_id == step_id:
                return resolved_step
        raise KeyError(f"Unknown resolved step ID for variant {variant}: {step_id}")

    def validate_domain(self, domain: str) -> ValidationReport:
        return self._validator.validate_domain(domain)

    def get_phase_graph(
        self,
        domain: str,
        phase: str,
        *,
        variant: str = "elective",
        format: str = "reactflow",
    ) -> dict[str, object]:
        steps = self.list_steps(domain, phase=phase, variant=variant)
        return self._graph_generator.generate(
            steps,
            phase=phase,
            variant=variant,
            format=format,
        )

    def _to_resolved_step(self, step: BaselineStep) -> ResolvedStep:
        return ResolvedStep(
            resolved_step_key=f"{step.domain}:elective:{step.baseline_step_id}",
            domain=step.domain,
            phase=step.phase,
            baseline_step_id=step.baseline_step_id,
            variant_step_id=None,
            variant="elective",
            title=step.title,
            roles=step.roles,
            items=step.items,
            warnings=step.warnings,
            node_type=step.node_type,
            refs=step.refs,
        )