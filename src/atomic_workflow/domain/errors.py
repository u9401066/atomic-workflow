from __future__ import annotations


class AtomicWorkflowError(Exception):
    """Base exception for the Atomic Workflow core engine."""


class ParseError(AtomicWorkflowError):
    """Raised when markdown content cannot be parsed into domain objects."""


class StepFormatError(ParseError):
    """Raised when a step section violates the expected markdown contract."""


class DuplicateStepError(AtomicWorkflowError):
    """Raised when the same step ID appears more than once in a domain."""


class StepNotFoundError(AtomicWorkflowError):
    """Raised when the requested step ID does not exist."""


class DomainNotFoundError(AtomicWorkflowError):
    """Raised when the requested workflow domain does not exist."""


class VariantNotFoundError(AtomicWorkflowError):
    """Raised when the requested workflow variant does not exist."""