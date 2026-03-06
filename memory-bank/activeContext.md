# Active Context

## Current Focus

**互動式 MVP 已完成建構。** Python core engine（parser → resolver → validator → graph → MCP → CLI）+ VS Code extension（TreeView + React Flow webview）全部可建構。

已完成的完整實作堆疊：

- **Python Core Engine**：domain models、baseline/variant parser、resolver、repository、service facade、validator、graph generator、serialization、CLI、MCP server（6 read tools）
- **VS Code Extension**：extension host（TreeView + EditorPanel + McpClient）、React 19 + React Flow webview（StepNode + DecisionNode custom nodes）
- **Tests**：16/16 通過（4 unit + 4 integration suites）
- **Build**：esbuild (extension host)、Vite (webview-ui) 全部建構成功
- **Git**：3 個結構化 commits 已推送

## Recently Changed Files

- `src/atomic_workflow/` — 完整 Python core engine
- `tests/` — 16 個測試（unit + integration）
- `extension/` — VS Code extension host + React Flow webview
- `pyproject.toml` — scripts + dependencies
- `.github/*.chatmode.md` — agent chatmode definitions

## Current Blockers

- None
