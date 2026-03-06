# Active Context

## Current Focus

**互動式 MVP 完成並驗證。** Python core engine + VS Code extension + VSIX 打包 + 端對端驗證 全數通過。

已完成的完整實作堆疊：

- **Python Core Engine**：domain models、baseline/variant parser、resolver、repository、service facade、validator、graph generator、serialization、CLI、MCP server（6 read tools）
- **VS Code Extension**：extension host（TreeView + EditorPanel + McpClient）、React 19 + React Flow webview（StepNode + DecisionNode custom nodes）
- **Tests**：16/16 Python 測試通過 + React webview-ui 測試完成
- **Build**：esbuild (extension host)、Vite (webview-ui) 全部建構成功
- **VSIX**：atomic-workflow-0.1.0.vsix (537.53 KB) 已打包並安裝驗證
- **Git**：結構化 commits 已推送

## Recently Changed Files

- `extension/.vscodeignore` — 新增 VSIX 打包排除規則
- `extension/LICENSE` — 複製自專案根目錄
- `extension/package.json` — 新增 vitest, vsce, coverage 依賴；升級 esbuild
- `extension/webview-ui/package.json` — 新增測試依賴

## Current Blockers

- None
