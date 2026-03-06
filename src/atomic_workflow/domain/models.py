from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, TypeAlias

NodeType: TypeAlias = Literal[
    "task",
    "decision",
    "parallel_start",
    "parallel_end",
    "subprocess",
    "event",
    "milestone",
]
StepOrigin: TypeAlias = Literal[
    "baseline",
    "modified",
    "variant_only",
    "replacement",
]
ValidationSeverity: TypeAlias = Literal["error", "warning", "info"]
GraphNodeKind: TypeAlias = Literal[
    "baseline",
    "modified",
    "variant_only",
    "replacement",
    "skipped",
    "narrative",
]
GraphEdgeType: TypeAlias = Literal[
    "sequential",
    "variant_replace",
    "variant_insert_after",
    "triggers",
    "depends_on",
    "parallel_with",
    "uses_output_of",
    "shares_resource",
    "escalates_to",
    "compensates",
]
StepRefType: TypeAlias = Literal[
    "triggers",
    "depends_on",
    "parallel_with",
    "uses_output_of",
    "shares_resource",
    "escalates_to",
    "compensates",
]
VariantOperationType: TypeAlias = Literal["inherit", "modify", "skip", "add"]


@dataclass(slots=True)
class StepItem:
    text: str
    children: list["StepItem"] = field(default_factory=list)
    is_warning: bool = False


@dataclass(slots=True)
class RoleAssignment:
    role_code: str
    display_text: str
    qualifier: str | None = None


@dataclass(slots=True)
class StepReference:
    target: str
    type: StepRefType
    condition: str | None = None
    description: str | None = None


@dataclass(slots=True)
class BaselineStep:
    baseline_step_id: str
    domain: str
    phase: str
    sequence: int
    title: str
    roles: list[RoleAssignment]
    items: list[StepItem]
    warnings: list[str]
    tags: list[str]
    node_type: NodeType = "task"
    refs: list[StepReference] = field(default_factory=list)
    section: str | None = None
    source_file: str = ""
    source_variant: str = "elective"
    prev_step_id: str | None = None
    next_step_id: str | None = None


@dataclass(slots=True)
class VariantOperation:
    variant: str
    phase: str | None
    operation: VariantOperationType
    applies_to: list[str] = field(default_factory=list)
    variant_step_id: str | None = None
    title: str | None = None
    rationale: str | None = None
    content_items: list[StepItem] | None = None
    roles: list[RoleAssignment] | None = None
    source_file: str | None = None
    order: int = 0


@dataclass(slots=True)
class WorkflowGraphNode:
    node_id: str
    label: str
    phase: str
    variant: str
    kind: GraphNodeKind
    node_type: NodeType = "task"
    refs: list[StepReference] = field(default_factory=list)
    source_file: str | None = None


@dataclass(slots=True)
class WorkflowGraphEdge:
    source: str
    target: str
    edge_type: GraphEdgeType
    condition: str | None = None
    description: str | None = None


@dataclass(slots=True)
class ValidationIssue:
    severity: ValidationSeverity
    code: str
    message: str
    file: str
    line: int | None = None
    step_id: str | None = None


@dataclass(slots=True)
class ValidationReport:
    domain: str
    valid: bool
    errors: list[ValidationIssue] = field(default_factory=list)
    warnings: list[ValidationIssue] = field(default_factory=list)
    infos: list[ValidationIssue] = field(default_factory=list)
    stats: dict[str, int] = field(default_factory=dict)


@dataclass(slots=True)
class ResolvedStep:
    resolved_step_key: str
    domain: str
    phase: str
    baseline_step_id: str | None
    variant_step_id: str | None
    variant: str
    title: str
    roles: list[RoleAssignment]
    items: list[StepItem]
    warnings: list[str]
    origin: StepOrigin = "baseline"
    supersedes: list[str] = field(default_factory=list)
    node_type: NodeType = "task"
    refs: list[StepReference] = field(default_factory=list)

    @property
    def step_id(self) -> str:
        if self.baseline_step_id is not None:
            return self.baseline_step_id
        if self.variant_step_id is not None:
            return self.variant_step_id
        raise ValueError("ResolvedStep must have either baseline_step_id or variant_step_id")