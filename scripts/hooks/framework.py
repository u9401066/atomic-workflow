from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True, slots=True)
class CheckResult:
    success: bool
    summary: str
    details: tuple[str, ...] = field(default_factory=tuple)

    @property
    def exit_code(self) -> int:
        return 0 if self.success else 1


def run_git_command(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=True,
        cwd=PROJECT_ROOT,
    )
    return result.stdout.strip()


def get_staged_files(diff_filter: str = "ACMR") -> list[str]:
    output = run_git_command(["diff", "--cached", "--name-only", f"--diff-filter={diff_filter}"])
    return [line for line in output.splitlines() if line]


def is_path_exempt(filepath: str, patterns: Iterable[str]) -> bool:
    return any(filepath == pattern or filepath.startswith(pattern) for pattern in patterns)


def emit(result: CheckResult) -> int:
    print(result.summary)
    for detail in result.details:
        print(detail)
    return result.exit_code