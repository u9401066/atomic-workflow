# Progress (Updated: 2026-03-06)

## Done

- 完成 atomic-workflow 第一批可提交實作切片分析，確認建議以 baseline-only read path + 最小 hook framework 作為首批落地範圍
- 已建立第一批實作骨架：src/atomic_workflow domain models、baseline parser、step index、workflow repository、workflow service、mcp scaffold、scripts/hooks/framework.py、對應 unit/integration tests
- 已驗證 baseline-only 垂直切片可運作：`uv run pytest` 目標測試 10/10 通過
- 已修正測試入口陷阱：新增 `[project.scripts].test`，`uv run test` 與 `uv run pytest` 皆可執行；移除 deprecated 的 `[tool.uv].dev-dependencies` 設定
- 已完成第二批 read-path 實作：variant parser、minimal variant resolver、repository/service variant 支援
- 已支援真實 corpus 中的 marker-less H3 narrative fallback；無 emoji 的 variant heading 先視為 `modify` overlay，避免整份 variant 檔解析失敗
- 已驗證目前完整測試集：`uv run test` 共 13/13 通過
- 已建立 validator（BL_*/VAR_* structural checks）+ graph generator（reactflow-compatible JSON）
- 已建立 CLI（6 commands）+ MCP server（6 read tools via FastMCP stdio）
- 已建立 VS Code extension：TreeView + WebviewPanel + React Flow interactive graph
- Extension 建構驗證通過：esbuild → dist/extension.js (14kb)、Vite → dist/webview/ (381kb + 16kb CSS)
- 全部 16/16 Python 測試通過
- 已推送 3 個結構化 commits：core engine + tests + extension

## Doing

- 無

## Next

- Extension 端對端測試（安裝到 VS Code 驗證 TreeView 與 Webview 載入）
- MCP write tools（§11.5 的 17 個寫入工具）
- Streamlit dashboard（Phase 2）
