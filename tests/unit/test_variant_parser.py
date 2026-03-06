from __future__ import annotations

from pathlib import Path

from atomic_workflow.parser import VariantParser


def test_variant_parser_extracts_add_modify_skip_and_ranges() -> None:
    content = """# 🟡 U 刀（Urgent）流程

## Phase A：術前評估

### [A-01] 接到照會 ⚡改

- 立即通知麻醉醫師

### [A-02] ~ [A-03] ✅同基線

> 維持基線

### [A-U01] 加快抽血流程 🆕

- 加速抽血
- ⚠️ 確認檢驗送出

### [A-04] ⏭️跳過

> 不執行
"""

    operations = VariantParser().parse(content, source_file=Path("urgent.md"))

    assert [operation.operation for operation in operations] == ["modify", "inherit", "add", "skip"]
    assert operations[0].applies_to == ["A-01"]
    assert operations[0].content_items is not None
    assert operations[1].applies_to == ["A-02", "A-03"]
    assert operations[2].variant_step_id == "A-U01"
    assert operations[2].content_items is not None
    assert operations[2].content_items[1].is_warning is True
    assert operations[3].applies_to == ["A-04"]