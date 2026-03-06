# Copilot 自定義指令 — Atomic Workflow

此文件為 VS Code GitHub Copilot 提供專案上下文與操作規範。

---

## 專案概述

**Atomic Workflow** — 將臨床工作流程原子化為結構化 Markdown 檔案，使其可版本控制、可驗證、可 AI 存取。

- **核心理念**：臨床工作流程 = 結構化原始碼（非資料庫）
- **唯一規格**：`SPEC.md` 是完整的實作契約（~2400+ 行）
- **資料存儲**：Structured Markdown Files, Not Database（§0.4）
- **架構**：baseline + variant overlay 模式

### 三層價值

| Layer | Phase | 目標 |
|-------|-------|------|
| Redesign | Phase 1 (MVP) | 分解、重構、比較工作流程變體 |
| Dashboard | Phase 2 | Streamlit 視覺化指標、差異比較 |
| Runtime Monitor | Phase 3 (future) | 即時追蹤工作流程執行 |

### Phase 1 MVP 範圍

1. 解析 `baseline` 文件 + `variant` overlay
2. Python core engine (parser → resolver → validator → graph)
3. MCP tools for Copilot（6 read + 17+ write）
4. VS Code extension (tree view, interactive node editor, compare, inspector)
5. 結構化回寫：UI 操作 → `.md` 檔案

---

## 開發哲學

> **「想要寫文件的時候，就更新 Memory Bank 吧！」**
>
> **「想要零散測試的時候，就寫測試檔案進 tests/ 資料夾吧！」**

- `SPEC.md` 是唯一的實作規格來源（修改程式碼前先更新規格）
- 程式碼是文檔的「編譯產物」
- 不要另開檔案寫筆記，直接寫進 Memory Bank

---

## 法規層級

```
CONSTITUTION.md          ← 最高原則（不可違反）
  │
  ├── .github/bylaws/    ← 子法（細則規範）
  │     ├── ddd-architecture.md
  │     ├── git-workflow.md
  │     ├── python-environment.md
  │     └── memory-bank.md
  │
  └── SPEC.md            ← 技術規格契約
```

你必須遵守以下法規層級：
1. **憲法**：`CONSTITUTION.md` - 最高原則，不可違反
2. **子法**：`.github/bylaws/*.md` - 細則規範
3. **規格**：`SPEC.md` - 完整技術規格（實作細節的唯一來源）

---

## 架構原則

### 目錄結構

```text
atomic-workflow/
├── workflows/                    # 📂 Source-of-truth markdown corpus
│   └── anesthesia/
│       ├── baseline/             #   phase-a-preop.md ... phase-l-postop.md
│       └── variants/             #   emergency.md, urgent.md, day-surgery.md
├── src/
│   └── atomic_workflow/          # 🐍 Python core engine
│       ├── domain/               #   dataclasses: BaselineStep, ResolvedStep
│       ├── parser/               #   baseline + variant parsers (§5)
│       ├── resolver/             #   variant overlay resolver (§7)
│       ├── validation/           #   ValidationReport builder (§8)
│       ├── graph/                #   graph generator (§9)
│       ├── services/             #   WorkflowService facade (§10.4)
│       ├── repository/           #   WorkflowRepository impl (§12)
│       └── mcp/                  #   MCP tool handlers (§11)
├── extension/                    # 🧩 VS Code extension (TypeScript)
├── tests/                        # pytest (unit + integration)
├── schemas/                      # JSON Schema (§4.2, §4.3)
├── streamlit/                    # Phase 2 dashboard (deferred)
├── SPEC.md                       # 技術規格契約
├── pyproject.toml                # Python config (uv)
└── .pre-commit-config.yaml
```

### 依賴方向

VS Code Extension → (MCP stdio) → Python Core Engine → Markdown Files

Python 內部：`services/ → parser/ + resolver/ + validation/ + graph/ → domain/ + repository/`

---

## 技術棧

### Python Core Engine (≥ 3.12)
- **套件管理**：uv（優先於 pip）
- **YAML**：PyYAML + ruamel.yaml（frontmatter 讀寫，roundtrip 保留格式）
- **Schema**：jsonschema（frontmatter 驗證）
- **MCP**：mcp SDK ≥ 1.0（stdio transport）
- **品質**：ruff (lint+format), mypy --strict, pytest, bandit

### VS Code Extension (TypeScript ≥ 5.4)
- esbuild bundler
- React 19 + @xyflow/react (interactive node editor webview)
- Vite (webview bundler)
- Tailwind CSS (webview styling)

### 安裝 & 初始化

```bash
uv venv
uv sync --all-extras
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg
```

---

## Memory Bank 同步

每次重要操作必須更新 Memory Bank：

| 操作 | 更新文件 |
|------|----------|
| 完成任務 | `progress.md` (Done) |
| 開始任務 | `progress.md` (Doing), `activeContext.md` |
| 重大決策 | `decisionLog.md` |
| 架構變更 | `architect.md` |

詳見：`.github/bylaws/memory-bank.md`

---

## Git 工作流

提交前必須執行檢查清單：
1. ✅ Memory Bank 同步（必要）
2. 📖 README 更新（如需要）
3. 📋 CHANGELOG 更新（如需要）

### Pre-commit Hooks

| Hook | 描述 |
|------|------|
| ruff (lint+format) | Python 程式碼品質 |
| mypy | 型別檢查（src/ only） |
| bandit | 安全掃描（src/ only） |
| gitleaks | Secrets 偵測 |
| conventional-pre-commit | Commit message 格式 |
| commit-size-guard | 限制每次 commit ≤ 30 檔案 |
| memory-bank-reminder | 提醒同步 Memory Bank |
| agent-freshness-check | 檢查 Agent 模型/工具是否過時 |

詳見：`.github/bylaws/git-workflow.md`

---

## Memory Checkpoint 規則

### 主動觸發時機
1. 對話超過 **10 輪**
2. 累積修改超過 **5 個檔案**
3. 完成一個 **重要功能/修復**
4. 使用者說要 **離開/等等**

### 必須記錄
- 當前工作焦點
- 變更的檔案列表（完整路徑）
- 待解決事項
- 下一步計畫

---

## Copilot Agents

位於 `.github/agents/`：

| Agent | 用途 | 預設模型 |
|-------|------|----------|
| `architect` | 系統架構設計 + Memory Bank | Claude Sonnet 4.6 |
| `code` | 實作功能 + 程式碼編寫 | Claude Sonnet 4.6 |
| `ask` | 專案問答 + 知識查詢 | GPT-4.1 |
| `debug` | 除錯分析 + 問題修復 | Claude Sonnet 4.6 |
| `audit` | 深度程式碼審計 | Claude Opus 4.6 |
| `orchestrator` | 拆解需求、委派、追蹤 | Claude Opus 4.6 |
| `deep-thinker` | 深度推理 — 算法、根因、架構權衡 | Claude Opus 4.6 |
| `researcher` | 只讀探索 — codebase 調查 | Gemini 3.1 Pro |
| `research` | PubMed 文獻搜尋 + Zotero 管理 | (MCP tools) |
| `test-runner` | 跑測試 + 迭代修復 | GPT-5 mini |
| `context-loader` | 讀取 Memory Bank + codebase 摘要 | GPT-4.1 |
| `review-panel` | 多模型審查委員會（3 AI 交叉審查） | Claude Opus 4.6 |

### 免費模型策略
- **重複性高、嘗試次數多**的工作用免費模型（test-runner, context-loader, ask）
- **需要推理和判斷**的工作用付費模型（architect, code, audit）

### Subagent 優先原則

**盡量將工作委派給 subagent，而非在主對話中直接執行。**

原因：
- **記憶壓縮**：subagent 啟動時會讀取 Memory Bank + copilot-instructions，等於自動載入專案上下文，不佔用主對話的 token 額度
- **上下文實體化**：每個 subagent 呼叫都有獨立的 context window，避免主對話因累積過多中間結果而溢出
- **平行處理**：獨立的子任務可以委派給不同 subagent，各自有完整的記憶存取能力
- **成本優化**：用免費模型的 subagent（test-runner, context-loader, ask）處理重複性工作，節省付費 token

適合委派的場景：
| 場景 | 推薦 Agent |
|------|-----------|
| 搜尋 codebase、閱讀多檔案 | `researcher` / `Explore` |
| 跑測試 + 修復迴圈 | `test-runner` |
| 載入 Memory Bank 整理摘要 | `context-loader` |
| 架構決策需要深度推理 | `deep-thinker` |
| 跨模組大型任務拆解 | `orchestrator` |
| 程式碼審查 | `review-panel` |

不適合委派的場景：
- 簡單的單檔編輯（直接做比委派更快）
- 需要與使用者即時互動確認的操作
- 涉及破壞性操作（刪除、force push）需主對話確認

---

## Copilot Prompts

位於 `.github/prompts/`：

| Prompt | 用途 |
|--------|------|
| `code-audit.prompt.md` | 深度程式碼審計 |
| `code-review.prompt.md` | 快速程式碼審查 |
| `pre-commit.prompt.md` | 提交前工作流 |
| `security-scan.prompt.md` | 安全掃描 |
| `skill-health-check.prompt.md` | Skill 翻新檢查 |

---

## SPEC 快速參照

| 章節 | 內容 |
|------|------|
| §1-3 | Step 定義、ID 規則、角色/裝備 |
| §4 | YAML frontmatter schema + 防禦性設計 |
| §5 | Baseline parser |
| §6 | Variant overlay 格式 |
| §7 | Variant resolver |
| §8 | Validation rules |
| §9 | Graph generator |
| §10 | Package architecture + WorkflowService |
| §11 | MCP tool interface (17+ tools) |
| §12 | Data Access Layer (repository) |
| §13 | VS Code extension |
| §14-16 | Migration, non-goals, MVP DoD |
| §17 | Runtime monitor (future) |
| §18 | Extensibility assessment |

---

## 可用的 MCP Servers

### Zotero + PubMed（研究用途）
- 使用 `@research` agent 進行文獻搜尋
- 文獻搜尋（PICO 策略）、引用分析、全文存取
- Zotero 書目管理

---

## 回應風格

- 使用**繁體中文**
- 提供清晰的步驟說明
- 引用 SPEC.md 章節號（如 §4.2, §10.4）
- 執行操作後更新 Memory Bank
- 遵循 Conventional Commits 格式

## 💡 研究模式
切換到 **@research** agent 可獲得完整的文獻搜尋助理功能，包括 PICO 搜尋、引用網路、全文取得等進階功能。

## 回應風格
- 使用繁體中文
- 清楚說明每個步驟
- 匯入前確認用戶意圖
