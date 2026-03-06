from __future__ import annotations

import pytest

from scripts.hooks import framework


def test_is_path_exempt_matches_exact_and_prefix() -> None:
    patterns = ["uv.lock", "memory-bank/", "htmlcov/"]

    assert framework.is_path_exempt("uv.lock", patterns) is True
    assert framework.is_path_exempt("memory-bank/progress.md", patterns) is True
    assert framework.is_path_exempt("src/atomic_workflow/domain/models.py", patterns) is False


def test_get_staged_files_uses_git_output(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_run_git_command(args: list[str]) -> str:
        assert args == ["diff", "--cached", "--name-only", "--diff-filter=ACMR"]
        return "src/atomic_workflow/domain/models.py\nmemory-bank/progress.md\n"

    monkeypatch.setattr(
        framework,
        "run_git_command",
        fake_run_git_command,
    )

    assert framework.get_staged_files() == [
        "src/atomic_workflow/domain/models.py",
        "memory-bank/progress.md",
    ]