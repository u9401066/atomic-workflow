"""Commit Size Guard — 限制每次 commit 的檔案數量。

規則：
- 最多 30 個檔案（豁免 uv.lock、htmlcov/、memory-bank/）
- 超過限制時阻擋 commit，提示拆分
- 緊急繞過：git commit --no-verify
"""

from __future__ import annotations

import sys

from scripts.hooks.framework import CheckResult, emit, get_staged_files, is_path_exempt

MAX_FILES = 30
EXEMPT_PATTERNS = [
    "uv.lock",
    "htmlcov/",
    "memory-bank/",
    ".pre-commit-config.yaml",
]


def main() -> int:
    staged = get_staged_files()
    counted = [f for f in staged if not is_path_exempt(f, EXEMPT_PATTERNS)]

    if len(counted) > MAX_FILES:
        return emit(
            CheckResult(
                success=False,
                summary=f"❌ Commit 包含 {len(counted)} 個檔案（上限 {MAX_FILES}）",
                details=(
                    "   豁免項目不計入：uv.lock, htmlcov/, memory-bank/",
                    "",
                    "📋 建議：",
                    "   1. 拆分為多個 focused commits",
                    "   2. 使用 git add -p 部分暫存",
                    "   3. 緊急繞過：git commit --no-verify",
                ),
            )
        )

    if counted:
        return emit(
            CheckResult(
                success=True,
                summary=f"✅ Commit 大小合規：{len(counted)}/{MAX_FILES} 檔案",
            )
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
