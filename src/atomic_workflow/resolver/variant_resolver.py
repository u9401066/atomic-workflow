from __future__ import annotations

from collections import defaultdict

from atomic_workflow.domain.models import BaselineStep, ResolvedStep, StepItem, VariantOperation


class VariantResolver:
    """Resolve baseline steps plus variant operations into ResolvedStep objects."""

    def resolve(
        self,
        baseline_steps: list[BaselineStep],
        operations: list[VariantOperation],
        *,
        variant: str,
    ) -> list[ResolvedStep]:
        by_phase: dict[str, list[BaselineStep]] = defaultdict(list)
        for step in baseline_steps:
            by_phase[step.phase].append(step)

        operations_by_phase: dict[str, list[VariantOperation]] = defaultdict(list)
        for operation in sorted(operations, key=lambda item: item.order):
            if operation.phase is not None:
                operations_by_phase[operation.phase].append(operation)

        resolved: list[ResolvedStep] = []
        for phase in sorted(by_phase):
            resolved.extend(
                self._resolve_phase(
                    by_phase[phase],
                    operations_by_phase.get(phase, []),
                    variant=variant,
                )
            )
        return resolved

    def _resolve_phase(
        self,
        phase_steps: list[BaselineStep],
        operations: list[VariantOperation],
        *,
        variant: str,
    ) -> list[ResolvedStep]:
        resolved: list[ResolvedStep] = []
        baseline_by_id = {step.baseline_step_id: step for step in phase_steps}
        cursor = 0

        for operation in operations:
            if operation.operation == "add":
                resolved.append(self._resolve_add(operation, phase_steps[0].domain, variant, phase_steps[0].phase))
                continue

            target_ids = [step_id for step_id in operation.applies_to if step_id in baseline_by_id]
            if not target_ids:
                continue

            first_target = target_ids[0]
            while cursor < len(phase_steps) and phase_steps[cursor].baseline_step_id != first_target:
                resolved.append(self._resolve_baseline(phase_steps[cursor], variant))
                cursor += 1

            for target_index, target_id in enumerate(target_ids):
                if cursor < len(phase_steps) and phase_steps[cursor].baseline_step_id == target_id:
                    step = phase_steps[cursor]
                    cursor += 1
                else:
                    step = baseline_by_id[target_id]

                if operation.operation == "skip":
                    continue
                if operation.operation == "inherit":
                    resolved.append(self._resolve_baseline(step, variant))
                    continue
                resolved.append(
                    self._resolve_modify(
                        step,
                        operation,
                        variant=variant,
                        use_overlay=target_index == 0 and len(target_ids) == 1,
                    )
                )

        while cursor < len(phase_steps):
            resolved.append(self._resolve_baseline(phase_steps[cursor], variant))
            cursor += 1

        return resolved

    def _resolve_baseline(self, step: BaselineStep, variant: str) -> ResolvedStep:
        return ResolvedStep(
            resolved_step_key=f"{step.domain}:{variant}:{step.baseline_step_id}",
            domain=step.domain,
            phase=step.phase,
            baseline_step_id=step.baseline_step_id,
            variant_step_id=None,
            variant=variant,
            title=step.title,
            roles=step.roles,
            items=step.items,
            warnings=step.warnings,
            origin="baseline",
            node_type=step.node_type,
            refs=step.refs,
        )

    def _resolve_modify(
        self,
        step: BaselineStep,
        operation: VariantOperation,
        *,
        variant: str,
        use_overlay: bool,
    ) -> ResolvedStep:
        items = step.items
        warnings = step.warnings
        title = step.title

        if use_overlay and operation.content_items:
            items = operation.content_items
            warnings = self._collect_warnings(operation.content_items)
        if use_overlay and operation.title:
            title = operation.title

        return ResolvedStep(
            resolved_step_key=f"{step.domain}:{variant}:{step.baseline_step_id}",
            domain=step.domain,
            phase=step.phase,
            baseline_step_id=step.baseline_step_id,
            variant_step_id=None,
            variant=variant,
            title=title,
            roles=step.roles,
            items=items,
            warnings=warnings,
            origin="modified",
            node_type=step.node_type,
            refs=step.refs,
        )

    def _resolve_add(
        self,
        operation: VariantOperation,
        domain: str,
        variant: str,
        phase: str,
    ) -> ResolvedStep:
        items = operation.content_items or []
        return ResolvedStep(
            resolved_step_key=f"{domain}:{variant}:{operation.variant_step_id}",
            domain=domain,
            phase=phase,
            baseline_step_id=None,
            variant_step_id=operation.variant_step_id,
            variant=variant,
            title=operation.title or operation.variant_step_id or "variant-only-step",
            roles=[],
            items=items,
            warnings=self._collect_warnings(items),
            origin="variant_only",
        )

    def _collect_warnings(self, items: list[StepItem]) -> list[str]:
        warnings: list[str] = []

        def walk(nodes: list[StepItem]) -> None:
            for node in nodes:
                if node.is_warning:
                    warnings.append(node.text)
                walk(node.children)

        walk(items)
        return warnings