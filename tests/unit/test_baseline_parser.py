from __future__ import annotations

from pathlib import Path

from atomic_workflow.parser import BaselineParser


def test_parse_baseline_step_section_with_nested_items() -> None:
    content = """# Phase A：術前門診 / 照會

## A1. 接案

### [A-01] 接到麻醉照會單 / 術前門診排定 🆕
**執行者**：👨‍⚕️ 麻醉醫師 ／ 👩‍⚕️ 麻醉護理師（協助排程確認）

- 住院病人：主治醫師開立麻醉照會
- 👩‍⚕️ **麻醉護理師**：
  - 協助確認排程系統中照會已建立
  - ⚠️ 提前調閱病歷摘要供醫師審閱

### [A-02] 調閱電子病歷
**執行者**：👨‍⚕️ 麻醉醫師

- 查看門診紀錄
"""

    steps = BaselineParser().parse(
        content,
        domain="anesthesia",
        source_file=Path("phase-a-preop.md"),
    )

    assert [step.baseline_step_id for step in steps] == ["A-01", "A-02"]
    assert steps[0].tags == ["new"]
    assert steps[0].roles[0].role_code == "anesthesiologist"
    assert steps[0].roles[1].role_code == "nurse_anesthesia"
    assert steps[0].roles[1].qualifier == "協助排程確認"
    assert steps[0].items[1].children[1].is_warning is True
    assert steps[0].warnings == ["⚠️ 提前調閱病歷摘要供醫師審閱"]
    assert steps[0].next_step_id == "A-02"
    assert steps[1].prev_step_id == "A-01"