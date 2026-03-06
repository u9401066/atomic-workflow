from __future__ import annotations

import re
from pathlib import Path

from atomic_workflow.domain.errors import ParseError, StepFormatError
from atomic_workflow.domain.models import BaselineStep, RoleAssignment, StepItem

PHASE_HEADING_RE = re.compile(r"^#\s*Phase\s+(?P<phase>[A-Z])", re.MULTILINE)
STEP_HEADING_RE = re.compile(r"^###\s+\[(?P<step_id>[A-Z]-\d{2})\]\s*(?P<title>.+?)\s*$")
EXECUTOR_PREFIX_RE = re.compile(r"^\*\*執行者\*\*[：:]\s*(?P<roles>.+)$")
BULLET_RE = re.compile(r"^(?P<indent>\s*)-\s+(?P<text>.+)$")

ROLE_CODE_MAP: dict[str, str] = {
    "麻醉護理師": "nurse_anesthesia",
    "流動護理師": "nurse_circulating",
    "病房護理師": "nurse_ward",
    "PACU護理師": "nurse_pacu",
    "PACU 護理師": "nurse_pacu",
    "等候區護理師": "nurse_holding",
    "前台報到人員": "nurse_reception",
    "傳送人員": "transporter",
    "麻醉醫師": "anesthesiologist",
}


class BaselineParser:
    """Parse baseline markdown files into BaselineStep objects."""

    def parse(self, text: str, *, domain: str, source_file: Path) -> list[BaselineStep]:
        body = self._strip_frontmatter(text)
        phase = self._extract_phase(body, source_file)
        sections = self._split_step_sections(body)
        steps = [
            self._parse_step_section(section, domain=domain, phase=phase, source_file=source_file)
            for section in sections
        ]

        for index, step in enumerate(steps):
            if index > 0:
                step.prev_step_id = steps[index - 1].baseline_step_id
            if index < len(steps) - 1:
                step.next_step_id = steps[index + 1].baseline_step_id

        return steps

    def _strip_frontmatter(self, text: str) -> str:
        if not text.startswith("---\n"):
            return text

        delimiter_count = 0
        body_lines: list[str] = []
        for line in text.splitlines(keepends=True):
            if line.strip() == "---":
                delimiter_count += 1
                if delimiter_count == 2:
                    continue
            elif delimiter_count >= 2:
                body_lines.append(line)

        if delimiter_count < 2:
            raise ParseError("Unclosed frontmatter block")
        return "".join(body_lines)

    def _extract_phase(self, text: str, source_file: Path) -> str:
        match = PHASE_HEADING_RE.search(text)
        if match is None:
            raise ParseError(f"Missing phase H1 heading in {source_file}")
        return match.group("phase")

    def _split_step_sections(self, text: str) -> list[tuple[str, list[str]]]:
        sections: list[tuple[str, list[str]]] = []
        current_heading: str | None = None
        current_body: list[str] = []

        for line in text.splitlines():
            if line.startswith("### "):
                if current_heading is not None:
                    sections.append((current_heading, current_body))
                current_heading = line
                current_body = []
                continue
            if current_heading is not None:
                current_body.append(line)

        if current_heading is not None:
            sections.append((current_heading, current_body))

        return sections

    def _parse_step_section(
        self,
        section: tuple[str, list[str]],
        *,
        domain: str,
        phase: str,
        source_file: Path,
    ) -> BaselineStep:
        heading, body_lines = section
        heading_match = STEP_HEADING_RE.match(heading)
        if heading_match is None:
            raise StepFormatError(f"Invalid step heading: {heading}")

        step_id = heading_match.group("step_id")
        title = heading_match.group("title").strip()
        tags: list[str] = []
        if "🆕" in title:
            tags.append("new")
            title = title.replace("🆕", "").strip()

        content_lines = self._skip_step_yaml_block(body_lines)
        first_content_index = self._first_nonempty_index(content_lines)
        if first_content_index is None:
            raise StepFormatError(f"Step {step_id} is missing body content")

        executor_line = content_lines[first_content_index].strip()
        executor_match = EXECUTOR_PREFIX_RE.match(executor_line)
        if executor_match is None:
            raise StepFormatError(f"Step {step_id} is missing executor line")

        roles = self._parse_roles(executor_match.group("roles"))
        items = self._parse_items(content_lines[first_content_index + 1 :])
        warnings = self._collect_warnings(items)

        return BaselineStep(
            baseline_step_id=step_id,
            domain=domain,
            phase=phase,
            sequence=int(step_id.split("-")[1]),
            title=title,
            roles=roles,
            items=items,
            warnings=warnings,
            tags=tags,
            source_file=source_file.as_posix(),
        )

    def _skip_step_yaml_block(self, lines: list[str]) -> list[str]:
        first_nonempty_index = self._first_nonempty_index(lines)
        if first_nonempty_index is None:
            return lines
        if lines[first_nonempty_index].strip() != "```yaml":
            return lines

        remaining: list[str] = []
        in_yaml_block = True
        for line in lines[first_nonempty_index + 1 :]:
            if in_yaml_block and line.strip() == "```":
                in_yaml_block = False
                continue
            if not in_yaml_block:
                remaining.append(line)

        if in_yaml_block:
            raise StepFormatError("Unclosed step-level YAML block")
        return remaining

    def _first_nonempty_index(self, lines: list[str]) -> int | None:
        for index, line in enumerate(lines):
            if line.strip():
                return index
        return None

    def _parse_roles(self, roles_text: str) -> list[RoleAssignment]:
        assignments: list[RoleAssignment] = []
        segments = re.split(r"\s*[／/,，]\s*", roles_text)
        for segment in segments:
            normalized_segment = self._normalize_role_text(segment)
            qualifier = self._extract_qualifier(normalized_segment)
            if qualifier is not None:
                normalized_segment = normalized_segment.replace(f"（{qualifier}）", "")
                normalized_segment = normalized_segment.replace(f"({qualifier})", "")
            normalized_segment = normalized_segment.strip()
            if not normalized_segment:
                continue

            assignments.append(
                RoleAssignment(
                    role_code=self._role_code_for(normalized_segment),
                    display_text=normalized_segment,
                    qualifier=qualifier,
                )
            )

        if not assignments:
            raise StepFormatError(f"Unable to parse executor line: {roles_text}")
        return assignments

    def _normalize_role_text(self, text: str) -> str:
        normalized = text.replace("**", "").strip()
        normalized = normalized.replace("👨‍⚕️", "").replace("👩‍⚕️", "").replace("🚶", "")
        return re.sub(r"\s+", " ", normalized).strip()

    def _extract_qualifier(self, text: str) -> str | None:
        match = re.search(r"(?:（(?P<full>[^）]+)）|\((?P<ascii>[^)]+)\))$", text)
        if match is None:
            return None
        return match.group("full") or match.group("ascii")

    def _role_code_for(self, role_text: str) -> str:
        for label, code in ROLE_CODE_MAP.items():
            if label in role_text:
                return code
        return "unknown_role"

    def _parse_items(self, lines: list[str]) -> list[StepItem]:
        root_items: list[StepItem] = []
        stack: list[tuple[int, StepItem]] = []

        for line in lines:
            stripped = line.strip()
            if not stripped or stripped == "---" or line.startswith("## "):
                continue

            match = BULLET_RE.match(line)
            if match is None:
                if stack:
                    stack[-1][1].text = f"{stack[-1][1].text} {stripped}".strip()
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

    def _collect_warnings(self, items: list[StepItem]) -> list[str]:
        warnings: list[str] = []

        def walk(nodes: list[StepItem]) -> None:
            for node in nodes:
                if node.is_warning:
                    warnings.append(node.text)
                walk(node.children)

        walk(items)
        return warnings