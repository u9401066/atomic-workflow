from __future__ import annotations

from pathlib import Path

from atomic_workflow.domain.errors import DomainNotFoundError, StepNotFoundError, VariantNotFoundError
from atomic_workflow.domain.models import BaselineStep, VariantOperation
from atomic_workflow.parser import BaselineParser, VariantParser
from atomic_workflow.repository.step_index import StepIndex


class WorkflowRepository:
    def __init__(
        self,
        workflows_dir: Path,
        parser: BaselineParser | None = None,
        variant_parser: VariantParser | None = None,
    ) -> None:
        self._root = workflows_dir
        self._parser = parser or BaselineParser()
        self._variant_parser = variant_parser or VariantParser()
        self._index_cache: dict[str, StepIndex] = {}
        self._steps_cache: dict[str, dict[str, BaselineStep]] = {}
        self._variant_cache: dict[tuple[str, str], list[VariantOperation]] = {}

    def list_domains(self) -> list[str]:
        return sorted(
            path.name
            for path in self._root.iterdir()
            if path.is_dir() and (path / "baseline").exists()
        )

    def list_baseline_files(self, domain: str) -> list[Path]:
        baseline_dir = self._root / domain / "baseline"
        if not baseline_dir.exists():
            raise DomainNotFoundError(f"Unknown domain or missing baseline dir: {domain}")
        return sorted(baseline_dir.glob("*.md"))

    def load_baseline_file(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def parse_baseline_file(self, path: Path, *, domain: str) -> list[BaselineStep]:
        return self._parser.parse(self.load_baseline_file(path), domain=domain, source_file=path)

    def list_variant_files(self, domain: str) -> list[Path]:
        variants_dir = self._root / domain / "variants"
        if not variants_dir.exists():
            raise DomainNotFoundError(f"Unknown domain or missing variants dir: {domain}")
        return sorted(variants_dir.glob("*.md"))

    def list_variants(self, domain: str) -> list[str]:
        return [path.stem for path in self.list_variant_files(domain)]

    def parse_variant_file(self, path: Path) -> list[VariantOperation]:
        return self._variant_parser.parse(self.load_baseline_file(path), source_file=path)

    def list_variant_operations(
        self,
        domain: str,
        variant: str,
        *,
        force_rebuild: bool = False,
    ) -> list[VariantOperation]:
        cache_key = (domain, variant)
        if not force_rebuild and cache_key in self._variant_cache:
            return self._variant_cache[cache_key]

        variant_path = self._root / domain / "variants" / f"{variant}.md"
        if not variant_path.exists():
            raise VariantNotFoundError(f"Unknown variant: {variant}")

        operations = self.parse_variant_file(variant_path)
        self._variant_cache[cache_key] = operations
        return operations

    def build_step_index(self, domain: str, *, force_rebuild: bool = False) -> StepIndex:
        if not force_rebuild and domain in self._index_cache:
            return self._index_cache[domain]

        file_steps: list[tuple[Path, list[BaselineStep]]] = []
        steps_by_id: dict[str, BaselineStep] = {}
        for file_path in self.list_baseline_files(domain):
            steps = self.parse_baseline_file(file_path, domain=domain)
            file_steps.append((file_path, steps))
            for step in steps:
                steps_by_id[step.baseline_step_id] = step

        index = StepIndex.from_files(domain, file_steps)
        self._index_cache[domain] = index
        self._steps_cache[domain] = steps_by_id
        return index

    def list_baseline_steps(self, domain: str, *, phase: str | None = None) -> list[BaselineStep]:
        self.build_step_index(domain)
        steps = list(self._steps_cache[domain].values())
        if phase is not None:
            steps = [step for step in steps if step.phase == phase]
        return sorted(steps, key=lambda step: (step.phase, step.sequence))

    def get_baseline_step(self, domain: str, step_id: str) -> BaselineStep:
        self.build_step_index(domain)
        try:
            return self._steps_cache[domain][step_id]
        except KeyError as exc:
            raise StepNotFoundError(f"Unknown step ID: {step_id}") from exc

    def list_phases(self, domain: str) -> list[str]:
        return self.build_step_index(domain).list_phases()