# Atomic Workflow — Technical Specification

## 1. Vault Format Specification

### 1.1 File Naming Convention

```
phase-{letter}-{short-name}.md
```

- Letter: A-Z (uppercase in content, lowercase in filename)
- Short name: kebab-case English descriptor
- Examples: `phase-a-preop.md`, `phase-g-induction.md`

### 1.2 Step ID Format

```
{PHASE_LETTER}-{2-DIGIT_NUMBER}
```

- Phase letter: A-Z uppercase
- Number: 01-99, zero-padded
- Examples: `A-01`, `E-16`, `G-35`
- Uniqueness: Step ID is globally unique across all phases

### 1.3 Role Emoji Mapping

| Emoji | Role | Code |
|-------|------|------|
| 👨‍⚕️ | 麻醉醫師 | `ANESTHESIOLOGIST` |
| 👩‍⚕️ | 麻醉護理師 | `NURSE_ANESTHESIA` |
| 👩‍⚕️ | 流動護理師 | `NURSE_CIRCULATING` |
| 👩‍⚕️ | 病房護理師 | `NURSE_WARD` |
| 👩‍⚕️ | PACU護理師 | `NURSE_PACU` |
| 👩‍⚕️ | 等候區護理師 | `NURSE_HOLDING` |
| 👩‍⚕️ | 前台報到人員 | `NURSE_RECEPTION` |
| 🚶 | 傳送人員 | `TRANSPORTER` |

Note: 👩‍⚕️ is shared across nurse subtypes. Disambiguation is done via the text label following the emoji.

### 1.4 Markdown Structure Rules

1. **H1** (`#`): Phase title — one per file
2. **H2** (`##`): Section grouping (e.g., `## E1. 病人安頓`)
3. **H3** (`###`): Step definition — must start with `[STEP-ID]`
4. **Bold** (`**執行者**`): Role assignment line — must be the first line after H3
5. **Bullet list** (`-`): Action items
6. **Nested bullets** (`  -`): Sub-actions or details
7. **Warning prefix** (`⚠️`): Critical safety notes
8. **New step suffix** (`🆕`): Marks newly added steps

### 1.5 Variant Diff Notation

Variant files (emergency.md, urgent.md, day-surgery.md) use the following conventions:

| Symbol | Meaning |
|--------|---------|
| ✅ | Step included (same as baseline) |
| ⏭️ | Step skipped in this variant |
| ⚡ | Step modified (details follow) |
| 🆕 | Step unique to this variant |

---

## 2. Parser Specification

### 2.1 Parsing Pipeline

```
.md file → Read → Split by H3 → Extract Step ID → Extract Role
         → Extract Items → Extract Warnings → Build WorkflowNode
```

### 2.2 Regex Patterns

```python
# Step header
STEP_PATTERN = r'###\s+\[([A-Z]-\d{2})\]\s+(.+?)(?:\s+🆕)?$'

# Role line
ROLE_PATTERN = r'\*\*執行者\*\*：(.+)'

# Warning line
WARNING_PATTERN = r'^\s*-\s*⚠️\s*(.+)'

# Phase header
PHASE_PATTERN = r'^#\s+Phase\s+([A-Z])[：:]\s*(.+)'
```

### 2.3 YAML Frontmatter Schema

```json
{
  "type": "object",
  "required": ["domain", "phase", "phase_name", "step_range", "step_count"],
  "properties": {
    "domain": {"type": "string"},
    "phase": {"type": "string", "pattern": "^[A-Z]$"},
    "phase_name": {"type": "string"},
    "step_range": {"type": "string", "pattern": "^[A-Z]-\\d{2} ~ [A-Z]-\\d{2}$"},
    "step_count": {"type": "integer", "minimum": 1},
    "primary_roles": {"type": "array", "items": {"type": "string"}},
    "timing": {"type": "string"},
    "baseline": {"type": "string", "enum": ["elective", "emergency", "urgent", "day-surgery"]},
    "new_steps": {"type": "array", "items": {"type": "string"}},
    "prev_phase": {"type": ["string", "null"]},
    "next_phase": {"type": ["string", "null"]}
  }
}
```

---

## 3. MCP Server Specification

### 3.1 Transport

- Protocol: MCP (Model Context Protocol)
- Transport: stdio (VS Code ↔ Python process)
- Framework: `mcp` Python SDK

### 3.2 Tools Summary

| Tool | Input Schema | Output | Side Effects |
|------|-------------|--------|-------------|
| `query_step` | `{step_id: str}` | WorkflowNode JSON | None (read-only) |
| `list_steps` | `{phase?: str, role?: str, tag?: str}` | WorkflowNode[] JSON | None |
| `get_phase_graph` | `{phase: str, format: "mermaid"\|"json"}` | Graph data | None |
| `compare_variants` | `{phase: str, variants: str[]}` | Diff table (markdown) | None |
| `validate_workflow` | `{domain: str}` | ValidationReport JSON | None |
| `enrich_step` | `{step_id: str, source: str}` | Enriched data JSON | External DB read |

### 3.3 Tool Implementation Examples

```python
@server.tool()
async def query_step(step_id: str) -> str:
    """
    查詢工作流程中特定步驟的詳細資訊。
    
    Args:
        step_id: 步驟代碼，格式為 "{Phase}-{Number}"，如 "E-16"
    
    Returns:
        步驟的完整資訊，包含執行者、操作項目、注意事項。
    """
    node = parser.get_node(step_id)
    return node.to_json()

@server.tool()
async def get_phase_graph(phase: str, format: str = "mermaid") -> str:
    """
    取得特定 Phase 的流程圖。
    
    Args:
        phase: Phase 代碼（如 "G" 取得麻醉誘導流程圖）
        format: 輸出格式 — "mermaid"（Mermaid.js）或 "json"（D3.js 用）
    
    Returns:
        流程圖資料（Mermaid 語法或 JSON graph）。
    """
    graph = graph_engine.build_phase_graph(phase)
    if format == "mermaid":
        return graph.to_mermaid()
    return graph.to_json()

@server.tool()
async def enrich_step(step_id: str, source: str = "drug_db") -> str:
    """
    透過 DAL 連接外部資料庫，補充步驟相關資訊。
    
    Args:
        step_id: 步驟代碼
        source: 資料來源 — "drug_db" | "equipment_db" | "aims"
    
    Returns:
        外部資料庫的補充資訊。
    """
    node = parser.get_node(step_id)
    connector = dal.get_connector(source)
    return await connector.enrich(node)
```

### 3.4 Error Handling

- Step not found → `StepNotFoundError` with suggestion (fuzzy match)
- Phase not found → `PhaseNotFoundError` with valid phase list
- DAL connection failure → graceful degradation (return cached data or error message)

---

## 4. VSX Extension Specification

### 4.1 Activation Events

```json
{
  "activationEvents": [
    "workspaceContains:**/workflows/**/phase-*.md",
    "onView:atomicWorkflow.phaseTree",
    "onCommand:atomicWorkflow.openDashboard"
  ]
}
```

### 4.2 Commands

| Command | Title | Keybinding |
|---------|-------|------------|
| `atomicWorkflow.openDashboard` | Open Workflow Dashboard | `Ctrl+Shift+W D` |
| `atomicWorkflow.openFlowchart` | Open Phase Flowchart | `Ctrl+Shift+W F` |
| `atomicWorkflow.refreshTree` | Refresh Phase Tree | — |
| `atomicWorkflow.goToStep` | Go to Step by ID | `Ctrl+Shift+W G` |

### 4.3 Views

```json
{
  "views": {
    "atomicWorkflow": [
      {
        "id": "atomicWorkflow.phaseTree",
        "name": "Workflow Phases",
        "icon": "$(list-tree)"
      }
    ]
  }
}
```

### 4.4 Webview Communication

```
Extension ↔ Webview: postMessage / onDidReceiveMessage
Extension ↔ MCP Server: MCP client SDK
Webview renders: Mermaid.js (flowchart) / Chart.js (dashboard)
```

---

## 5. DAL Specification

### 5.1 Connector Interface

```python
from abc import ABC, abstractmethod

class WorkflowRepository(ABC):
    """工作流程 Repository 介面"""
    @abstractmethod
    def get_node(self, step_id: str) -> WorkflowNode: ...
    @abstractmethod
    def list_nodes(self, **filters) -> list[WorkflowNode]: ...
    @abstractmethod
    def get_phase(self, phase_id: str) -> Phase: ...
    @abstractmethod
    def get_workflow(self, domain: str, variant: str) -> Workflow: ...

class ExternalDataConnector(ABC):
    """外部資料來源 Connector 介面"""
    name: str
    @abstractmethod
    async def enrich(self, node: WorkflowNode) -> dict: ...
    @abstractmethod
    async def health_check(self) -> bool: ...
    @abstractmethod
    def get_capabilities(self) -> list[str]: ...
```

### 5.2 Data Source Registry

```python
registry = ConnectorRegistry()
registry.register('drug_db', DrugDBConnector(db_path='data/drugs.db'))
registry.register('equipment_db', EquipmentConnector(api_url='...'))
registry.register('aims', AIMSConnector(connection_string='...'))
```

### 5.3 Drug DB Schema (SQLite prototype)

```sql
CREATE TABLE drugs (
    id INTEGER PRIMARY KEY,
    generic_name TEXT NOT NULL,
    brand_name TEXT,
    category TEXT,
    concentration TEXT,
    typical_dose TEXT,
    max_dose TEXT,
    onset_time TEXT,
    duration TEXT,
    warnings TEXT,
    controlled_level INTEGER
);

CREATE TABLE equipment (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    sizes TEXT,
    location TEXT,
    check_items TEXT
);
```
