from __future__ import annotations

import re
from pathlib import Path

from atomic_workflow.domain.errors import DuplicateStepError, ParseError, StepFormatError
from atomic_workflow.domain.models import ValidationIssue, ValidationReport
from atomic_workflow.repository.workflow_repository import WorkflowRepository

BASELINE_FILENAME_RE = re.compile(r"^phase-(?P<letter>[a-z])-.*\.md$")


class WorkflowValidator:
    def __init__(self, repository: WorkflowRepository) -> None:
        self._repository = repository

    def validate_domain(self, domain: str) -> ValidationReport:
        errors: list[ValidationIssue] = []
        warnings: list[ValidationIssue] = []
        infos: list[ValidationIssue] = []

        try:
            baseline_files = self._repository.list_baseline_files(domain)
            self._repository.build_step_index(domain, force_rebuild=True)
        except DuplicateStepError as exc:
            errors.append(
                ValidationIssue(
                    severity="error",
                    code="BL_DUPLICATE_ID",
                    message=str(exc),
                    file=domain,
                )
            )
            return self._build_report(domain, errors, warnings, infos)

        all_issues: list[ValidationIssue] = []
        for baseline_file in baseline_files:
            all_issues.extend(self._validate_baseline_file(domain, baseline_file))
            all_issues.extend(self._validate_baseline_roles(domain, baseline_file))

        for variant in self._repository.list_variants(domain):
            all_issues.extend(self._validate_variant_file(domain, variant))

        for issue in all_issues:
            if issue.severity == "error":
                errors.append(issue)
            elif issue.severity == "warning":
                warnings.append(issue)
            else:
                infos.append(issue)

        return self._build_report(domain, errors, warnings, infos)

    def _validate_baseline_file(self, domain: str, path: Path) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        filename_match = BASELINE_FILENAME_RE.match(path.name)
        if filename_match is None:
            issues.append(
                ValidationIssue(
                    severity="error",
                    code="BL_FILENAME",
                    message=f"Invalid baseline filename: {path.name}",
                    file=path.as_posix(),
                )
            )
            return issues

        try:
            steps = self._repository.parse_baseline_file(path, domain=domain)
        except (ParseError, StepFormatError) as exc:
            issues.append(
                ValidationIssue(
                    severity="error",
                    code="BL_PARSE",
                    message=str(exc),
                    file=path.as_posix(),
                )
            )
            return issues

        expected_phase = filename_match.group("letter").upper()
        if steps and steps[0].phase != expected_phase:
            issues.append(
                ValidationIssue(
                    severity="error",
                    code="BL_H1_MISMATCH",
                    message=f"Filename phase {expected_phase} does not match parsed phase {steps[0].phase}",
                    file=path.as_posix(),
                )
            )

        previous_sequence = 0
        for step in steps:
            if step.sequence <= previous_sequence:
                issues.append(
                    ValidationIssue(
                        severity="warning",
                        code="BL_ORDER",
                        message=f"Step order is not strictly increasing at {step.baseline_step_id}",
                        file=path.as_posix(),
                        step_id=step.baseline_step_id,
                    )
                )
            previous_sequence = step.sequence

        return issues

    def _validate_baseline_roles(self, domain: str, path: Path) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        try:
            steps = self._repository.parse_baseline_file(path, domain=domain)
        except (ParseError, StepFormatError):
            return issues

        for step in steps:
            for role in step.roles:
                if role.role_code == "unknown_role":
                    issues.append(
                        ValidationIssue(
                            severity="warning",
                            code="BL_UNKNOWN_ROLE",
                            message=f"Unknown role label: {role.display_text}",
                            file=path.as_posix(),
                            step_id=step.baseline_step_id,
                        )
                    )
        return issues

    def _validate_variant_file(self, domain: str, variant: str) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        index = self._repository.build_step_index(domain)
        operations = self._repository.list_variant_operations(domain, variant, force_rebuild=True)
        variant_path = (self._repository._root / domain / "variants" / f"{variant}.md").as_posix()

        for operation in operations:
            if operation.operation == "add":
                continue
            for step_id in operation.applies_to:
                if not index.has_step(step_id):
                    issues.append(
                        ValidationIssue(
                            severity="error",
                            code="VAR_MISSING_STEP_REF",
                            message=f"Variant {variant} references unknown baseline step {step_id}",
                            file=variant_path,
                            step_id=step_id,
                        )
                    )
        return issues

    def _build_report(
        self,
        domain: str,
        errors: list[ValidationIssue],
        warnings: list[ValidationIssue],
        infos: list[ValidationIssue],
    ) -> ValidationReport:
        return ValidationReport(
            domain=domain,
            valid=not errors,
            errors=errors,
            warnings=warnings,
            infos=infos,
            stats={
                "errors": len(errors),
                "warnings": len(warnings),
                "infos": len(infos),
            },
        )