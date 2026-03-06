from __future__ import annotations

import re
from pathlib import Path
from typing import cast

from atomic_workflow.domain.errors import ParseError, StepFormatError
from atomic_workflow.domain.models import StepItem, VariantOperation, VariantOperationType

PHASE_HEADING_RE = re.compile(r"^##\s+Phase\s+(?P<phase>[A-Z])", re.MULTILINE)
STEP_ID_TOKEN_RE = re.compile(r"\[(?P<step_id>[A-Z]-[A-Z0-9]{2,})\]")
STANDARD_STEP_ID_RE = re.compile(r"^(?P<phase>[A-Z])-(?P<sequence>\d{2})$")
BULLET_RE = re.compile(r"^(?P<indent>\s*)-\s+(?P<text>.+)$")
MARKERS: dict[str, VariantOperationType] = {
    "✅": "inherit",
    "⚡": "modify",
    "⏭️": "skip",
    "🆕": "add",
}


class VariantParser:
    """Parse variant overlay markdown files into VariantOperation objects."""

    def parse(self, text: str, *, source_file: Path) -> list[VariantOperation]:
        variant = source_file.stem
        current_phase: str | None = None
        operations: list[VariantOperation] = []
        current_heading: str | None = None
        current_body: list[str] = []

        def flush_section() -> None:
            if current_heading is None or current_phase is None:
                return
            operations.append(
                self._parse_operation_section(
                    current_heading,
                    current_body,
                    phase=current_phase,
                    variant=variant,
                    source_file=source_file,
                    order=len(operations),
                )
            )

        for line in text.splitlines():
            phase_match = PHASE_HEADING_RE.match(line)
            if phase_match is not None:
                flush_section()
                current_heading = None
                current_body = []
                current_phase = phase_match.group("phase")
                continue

            if line.startswith("## "):
                flush_section()
                current_heading = None
                current_body = []
                current_phase = None
                continue

            if line.startswith("### "):
                flush_section()
                current_heading = line
                current_body = []
                continue

            if current_heading is not None:
                current_body.append(line)

        flush_section()

        if not operations:
            raise ParseError(f"No variant operations found in {source_file}")
        return operations

    def _parse_operation_section(
        self,
        heading: str,
        body_lines: list[str],
        *,
        phase: str,
        variant: str,
        source_file: Path,
        order: int,
    ) -> VariantOperation:
        step_ids = [match.group("step_id") for match in STEP_ID_TOKEN_RE.finditer(heading)]
        if not step_ids:
            raise StepFormatError(f"Invalid variant heading without step ids: {heading}")

        marker = self._extract_marker(heading)
        operation = cast(VariantOperationType, MARKERS[marker] if marker is not None else "modify")
        title = self._extract_title(heading, step_ids, marker)
        rationale = self._extract_rationale(body_lines)
        content_items = self._parse_items(body_lines)

        if operation == "add":
            return VariantOperation(
                variant=variant,
                phase=phase,
                operation="add",
                applies_to=[],
                variant_step_id=step_ids[0],
                title=title or step_ids[0],
                rationale=rationale,
                content_items=content_items,
                source_file=source_file.as_posix(),
                order=order,
            )

        applies_to = self._expand_targets(step_ids)
        return VariantOperation(
            variant=variant,
            phase=phase,
            operation=operation,
            applies_to=applies_to,
            title=title,
            rationale=rationale,
            content_items=content_items or None,
            source_file=source_file.as_posix(),
            order=order,
        )

    def _extract_marker(self, heading: str) -> str | None:
        for marker in MARKERS:
            if marker in heading:
                return marker
        return None

    def _extract_title(self, heading: str, step_ids: list[str], marker: str | None) -> str | None:
        normalized = heading[4:].strip()
        for step_id in step_ids:
            normalized = normalized.replace(f"[{step_id}]", "", 1)
        normalized = normalized.replace("~", " ")
        if marker is not None:
            marker_index = normalized.find(marker)
            if marker_index >= 0:
                normalized = normalized[:marker_index]
        title = " ".join(normalized.split()).strip()
        return title or None

    def _extract_rationale(self, body_lines: list[str]) -> str | None:
        text_lines = [
            line.strip().lstrip(">").strip()
            for line in body_lines
            if line.strip() and not line.lstrip().startswith("-")
        ]
        if not text_lines:
            return None
        return " ".join(text_lines)

    def _expand_targets(self, step_ids: list[str]) -> list[str]:
        if len(step_ids) == 1:
            return step_ids
        if len(step_ids) == 2:
            start_match = STANDARD_STEP_ID_RE.match(step_ids[0])
            end_match = STANDARD_STEP_ID_RE.match(step_ids[1])
            if start_match is not None and end_match is not None:
                start_phase = start_match.group("phase")
                end_phase = end_match.group("phase")
                if start_phase == end_phase:
                    start_number = int(start_match.group("sequence"))
                    end_number = int(end_match.group("sequence"))
                    return [f"{start_phase}-{number:02d}" for number in range(start_number, end_number + 1)]
        return step_ids

    def _parse_items(self, lines: list[str]) -> list[StepItem]:
        root_items: list[StepItem] = []
        stack: list[tuple[int, StepItem]] = []

        for line in lines:
            stripped = line.strip()
            if not stripped or stripped == "---":
                continue

            match = BULLET_RE.match(line)
            if match is None:
                continue

            indent = len(match.group("indent").replace("\t", "  "))
            level = indent // 2
            text_value = match.group("text").strip()
            item = StepItem(text=text_value, is_warning=text_value.startswith("⚠"))

            while stack and stack[-1][0] >= level:
                stack.pop()

            if stack:
                stack[-1][1].children.append(item)
            else:
                root_items.append(item)

            stack.append((level, item))

        return root_items