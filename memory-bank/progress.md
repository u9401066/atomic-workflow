# Progress (Updated: 2026-03-07)

## Done

- Updated SPEC.md to define a single-core, multi-client architecture with explicit VS Code and Streamlit client roles, boundaries, and MVP expectations.
- SPEC.md 完整 audit（2 輪，30 修正）+ 15 Mermaid diagrams
- §4.4 YAML Defensive Design（9 小節）
- §11.2 MCP CRUD 擴充至 17+ write tools + §11.5 Agent Safety Guardrails
- §12 DAL 擴充（read + write + snapshot/rollback）
- §0.6 Technology Stack（含 25 列 Completeness Verification Matrix）
- §18 Extensibility Assessment（11 成長軸）
- Template migration 完成：
  - `.editorconfig`, `.gitignore` 建立
  - `.pre-commit-config.yaml` 建立（py3.12, 12+ hooks）
  - `pyproject.toml` 建立（ruff, mypy strict, pytest, bandit, coverage 80%）
  - `scripts/hooks/` 搬遷（commit-size-guard, memory-bank-reminder, agent-freshness-check）
  - 14 Copilot agents 搬遷至 `.github/agents/`
  - `.github/bylaws/` 搬遷 + 客製化（ddd-architecture 改寫為 atomic-workflow 架構）
  - `.github/prompts/` 搬遷（5 prompt 檔）
  - `.github/copilot-instructions.md` 改寫（從 Zotero 自動生成 → 完整專案指令）
  - `.github/workflows/ci.yml` 客製化（移除 postgres/redis/Playwright，改用 uv，py3.12，加 extension build）
  - `CONSTITUTION.md` 客製化（適配 atomic-workflow 架構）
  - `ARCHITECTURE.md` 改寫（系統架構圖 + 模組對照表）
  - `python-environment.md` bylaw 更新為 Python 3.12+
  - SPEC §0.6.5 更新（加入 memory-bank, CONSTITUTION, .github/agents, bylaws, prompts）
  - 舊 `.chatmode.md` 檔案移除
  - template-ref 目錄清理

- SPEC.md §4.5 Step-level YAML Block schema（7 子節：格式、baseline/variant schema、v0 相容、validation pipeline、immutable fields、write-back rules）
- SPEC.md §4.6 Three-Layer Data Model（File Frontmatter / Step YAML / Step Markdown Body）
- SPEC.md §5.11 Step YAML Block Extraction（detection pattern + parsing pipeline + sync validation）
- SPEC.md §11.5.5 Write Hook Pipeline（8-stage strict hooks: 4 pre-write + 4 post-write）
- SPEC.md §11.5.6 Hook Audit Trail（HookLogEntry + .atomic-workflow/audit.jsonl）
- SPEC.md §12.4 StepIndex（in-memory lazy index + O(1) lookup + cache invalidation + performance targets）
- SPEC.md §13 完整改寫：mermaid.js read-only → React Flow interactive node editor
  - §13.1-13.2 架構圖更新（dual-process: Extension Host + Webview React App）
  - §13.2.1 Communication Protocol（postMessage typed envelopes）
  - §13.4 Commands 更新（openFlowchart → openEditor）
  - §13.5 MVP UI Components 擴充至 5 組件含完整互動行為
  - §13.6 React Flow Graph Contract（TypeScript interface 定義）
  - §13.7 Webview Build Pipeline（esbuild + Vite 雙 bundler）
  - §13.8 Theme Integration, §13.9 Manifest, §13.10 Performance Budget, §13.11 Keyboard Shortcuts
- SPEC.md §0.6 技術棧全面更新（React 19, @xyflow/react, Vite, Tailwind CSS）
- MCP `get_phase_graph` format: "mermaid" → "reactflow"
- copilot-instructions.md 更新（mermaid.js → React Flow）
- 跨引用更新（§0.3, §0.5 diagram, §10.6 deployment）
- SPEC.md BPMN-inspired extensions（§0.7 Concept Attribution + §2.3 Shared Process + §4.5.8-§4.5.9 node_type + refs + §6 Domain Model 更新 + §9 Graph schema 擴充 + §13.5.2/§13.6 React Flow 新 node/edge types + §18 Extensibility 大幅改寫）

## Doing

（無進行中任務）

## Next

- 開始實作 Python core engine（domain/ models → parser/ → resolver/）
- 建立 JSON Schema 檔案（schemas/baseline-frontmatter.json, variant-frontmatter.json）
- 初始化 VS Code extension scaffold（extension/ with React Flow）
- 初始化 uv 環境（`uv venv && uv sync --all-extras`）
