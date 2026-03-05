# Atomic Workflow

> **原子級工作流程再造平台** — VSX + MCP Architecture
>
> 將結構化 Markdown SOP 轉化為可視覺化、可查詢、可連接外部資料庫的智慧工作流程系統。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Vision

**Atomic Workflow** 將每一個作業流程拆解為不可再分的「原子步驟」（Atomic Steps），透過：

1. **Markdown Vault** — 結構化文件作為 Single Source of Truth
2. **MCP Server** — 解析、圖譜、查詢引擎
3. **VS Code Extension** — 流程圖 + Dashboard + Copilot 整合
4. **DAL Connectors** — 連接外部資料庫（AIMS / Drug DB / Equipment DB）

實現從 AS-IS 流程審計到 TO-BE 流程再造的完整生命週期。

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│  VS Code Extension (VSX)                        │
│  ├── 📄 Webview: 流程圖 (Mermaid.js / D3.js)    │
│  ├── 📊 Webview: Dashboard (統計/狀態總覽)       │
│  ├── 🌳 TreeView: 工作流程導覽 (Phase 樹狀)     │
│  ├── 🔗 DocumentLink: [[wikilink]] 點擊跳轉     │
│  └── 🤖 Copilot Chat Participant (via MCP)      │
└──────────────────┬──────────────────────────────┘
                   │ MCP Protocol (stdio)
┌──────────────────▼──────────────────────────────┐
│  MCP Server (Python)                            │
│  ├── Parser Layer   — MD → WorkflowNode 物件    │
│  ├── Graph Layer    — NetworkX 關係圖引擎        │
│  ├── Query Layer    — 步驟/角色/Phase 查詢      │
│  └── DAL Layer      — SQL/API connectors        │
│       ├── MarkdownRepo  (本地 vault 讀寫)       │
│       ├── AIMS          (麻醉資訊系統)          │
│       ├── DrugDB        (藥品資料庫)            │
│       └── EquipmentDB   (設備/耗材)             │
└─────────────────────────────────────────────────┘
         ↑
┌────────┴────────────────────────────────────────┐
│  Vault (Structured Markdown)                    │
│  ├── workflows/{domain}/baseline/*.md           │
│  ├── workflows/{domain}/variants/*.md           │
│  └── YAML Frontmatter + Step Format Spec        │
└─────────────────────────────────────────────────┘
```

### 設計原則

| 原則 | 說明 |
|------|------|
| **Markdown-First** | 流程定義存在 .md 檔案中，人類可讀、Git 可追蹤 |
| **DDD + DAL 分離** | Domain 物件（WorkflowNode）不依賴儲存實作 |
| **Copilot-Native** | Agent 透過 MCP Tools 與流程互動，不需自建 chat UI |
| **Multi-Domain** | 架構不綁定特定領域，可擴展至任何 SOP 場景 |
| **Atomic Granularity** | 每個步驟是不可再分的原子操作，有唯一 ID |

---

## 📐 Specification

### 1. Vault Format — Markdown 檔案規範

#### 1.1 YAML Frontmatter

每個 Phase 檔案頂部包含結構化 metadata：

```yaml
---
domain: anesthesia
phase: E
phase_name: 手術室內 — 病人安頓 & 監測建立
step_range: E-01 ~ E-17
step_count: 17
primary_roles:
  - 麻醉護理師
  - 麻醉醫師
  - 流動護理師
timing: 病人進入刀房 → 監測建立完成
baseline: elective
new_steps:
  - E-16
  - E-17
prev_phase: phase-d-holding.md
next_phase: phase-f-preparation.md
---
```

#### 1.2 Step Format（原子步驟格式）

```markdown
### [STEP-ID] 步驟名稱 {可選標籤}
**執行者**：{角色 emoji} {角色名稱}

- 操作項目 1
  - 子項目 a
  - 子項目 b
- 操作項目 2
- ⚠️ 注意事項
```

**規範**：
- `STEP-ID` = `{Phase Letter}-{2-digit number}`，如 `E-16`
- 角色 Emoji 固定映射：
  - 👨‍⚕️ = 麻醉醫師
  - 👩‍⚕️ = 護理師（含各類型）
  - 🚶 = 傳送人員
- ⚠️ 前綴 = 警告/注意事項
- 🆕 後綴 = 新增步驟標記

---

### 2. WorkflowNode Schema — 物件模型

```python
@dataclass
class WorkflowNode:
    """原子步驟的 Domain 物件"""
    id: str              # "E-16"
    phase: str           # "E"
    sequence: int        # 16
    name: str            # "開台前刀房環境準備"
    roles: list[Role]    # [Role.NURSE_ANESTHESIA]
    items: list[str]     # 操作項目（flat text）
    warnings: list[str]  # ⚠️ 注意事項
    is_new: bool         # 🆕 標記
    tags: list[str]      # 自由標籤
    prev_step: str | None
    next_step: str | None
    variant_diffs: dict[str, str]  # {"emergency": "skip", "urgent": "modified"}

class Role(Enum):
    ANESTHESIOLOGIST = "👨‍⚕️ 麻醉醫師"
    NURSE_ANESTHESIA = "👩‍⚕️ 麻醉護理師"
    NURSE_CIRCULATING = "👩‍⚕️ 流動護理師"
    NURSE_WARD = "👩‍⚕️ 病房護理師"
    NURSE_PACU = "👩‍⚕️ PACU護理師"
    NURSE_HOLDING = "👩‍⚕️ 等候區護理師"
    NURSE_RECEPTION = "👩‍⚕️ 前台報到人員"
    TRANSPORTER = "🚶 傳送人員"
```

---

### 3. MCP Server — Tools 設計

| Tool | 輸入 | 輸出 | 用途 |
|------|------|------|------|
| `query_step` | step_id: str | WorkflowNode JSON | 查詢步驟詳情 |
| `list_steps` | phase?, role?, tag? | WorkflowNode[] | 條件篩選步驟 |
| `get_phase_graph` | phase, format | Graph data | 取得 Phase 關係圖 |
| `compare_variants` | phase, variants[] | Diff table | 比較手術類型差異 |
| `validate_workflow` | domain | ValidationReport | 驗證完整性 |
| `enrich_step` | step_id, source | Enriched data | DAL 查詢補充資訊 |

#### MCP Server 設定

```json
// .vscode/mcp.json
{
  "servers": {
    "atomic-workflow": {
      "command": "uv",
      "args": ["run", "--directory", "${workspaceFolder}", "python", "-m", "atomic_workflow.server"],
      "env": {
        "VAULT_PATH": "${workspaceFolder}/workflows"
      }
    }
  }
}
```

---

### 4. DAL Layer — 資料存取層

```
DAL/
├── MarkdownRepository    ← 讀寫 .md vault（本地檔案系統）
├── AIMSConnector         ← 麻醉資訊系統（SQL Server / API）
├── DrugDBConnector       ← 藥品資料庫（SQLite / FHIR API）
└── EquipmentConnector    ← 設備耗材庫存（SQL / REST API）
```

---

## 📁 Repository Structure

```
atomic-workflow/
├── README.md                         ← 本文件（Project Spec）
├── SPEC.md                           ← 技術規格詳細文件
├── pyproject.toml                    ← Python 專案設定（uv）
├── LICENSE
├── .vscode/
│   └── mcp.json                      ← MCP Server 設定
│
├── workflows/                        ← Vault（結構化 Markdown）
│   └── anesthesia/                   ← 第一個 Domain：麻醉科
│       ├── README.md                 ← Domain 總覽 + 交叉比較矩陣
│       ├── baseline/                 ← 基線流程（12 Phases）
│       ├── variants/                 ← 手術類型變體
│       └── analysis/                 ← AI 分析文件
│
├── src/                              ← MCP Server (Python)
│   └── atomic_workflow/
│       ├── server.py                 ← MCP entry point
│       ├── parser/                   ← MD → WorkflowNode
│       ├── graph/                    ← NetworkX 圖譜引擎
│       ├── domain/                   ← Domain 物件
│       └── dal/                      ← Data Access Layer
│
├── vsx/                              ← VS Code Extension (TypeScript)
│   ├── package.json
│   └── src/
│
├── archive/                          ← 歷史文件存檔
└── schemas/                          ← 格式定義
```

---

## 🗺️ Roadmap

### Phase 1：Vault + Parser（MVP）
- [x] 建立 186 步原子級麻醉工作流程（12 Phases）
- [x] 建立 3 種手術變體（Emergency / Urgent / Day-Surgery）
- [ ] 加入 YAML frontmatter 到所有 .md 檔案
- [ ] 實作 Markdown Parser → WorkflowNode
- [ ] 實作 MCP Server 基礎工具（query_step, list_steps）

### Phase 2：Graph + Visualization
- [ ] NetworkX 圖譜引擎
- [ ] Mermaid.js 流程圖輸出
- [ ] MCP Tool: get_phase_graph
- [ ] VSX: Flowchart WebviewPanel

### Phase 3：Dashboard + TreeView
- [ ] VSX: Phase TreeView
- [ ] VSX: Dashboard WebviewPanel
- [ ] VSX: DocumentLink + Hover providers
- [ ] MCP Tool: validate_workflow

### Phase 4：DAL + Copilot
- [ ] DAL connector interfaces
- [ ] Drug DB connector（SQLite prototype）
- [ ] MCP Tool: enrich_step
- [ ] VSX: Copilot Chat Participant (@workflow)
- [ ] 擴展至第二個 Domain

---

## 📄 First Domain: Anesthesiology

| 指標 | 數值 |
|------|------|
| 總步驟數 | 186 |
| Phase 數 | 12（A~L） |
| 原始步驟 | 174 |
| 護理師新增步驟 | 12（🆕） |
| 手術變體 | 3（E刀/U刀/日間） |
| 角色類型 | 8 |

| Phase | 名稱 | 步驟數 |
|-------|------|--------|
| A | 術前評估 & 文件準備 | 14 |
| B | 病房 / 報到 — 術前準備 | 14 |
| C | 傳送至手術室 | 8 |
| D | 手術室等候區 | 9 |
| E | 手術室內 — 監測建立 | 17 |
| F | 麻醉準備 — 機器/藥物/氣道 | 21 |
| G | 麻醉誘導 | 36 |
| H | 手術擺位 & 手術開始 | 7 |
| I | 術中維持 | 26 |
| J | 甦醒 & 拔管 | 12 |
| K | PACU 恢復 | 13 |
| L | 術後追蹤 & 交班 | 10 |

---

## 📝 License

MIT License — see [LICENSE](LICENSE) for details.

## 👤 Author

**Tz Ping Gau** — Department of Anesthesiology, Kaohsiung Medical University Hospital
