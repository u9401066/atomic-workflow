# Architecture — Atomic Workflow

完整技術規格請見 `SPEC.md`。本文件提供高層架構概覽。

## 系統概覽

```
┌──────────────────────────────────────────────────────────┐
│                    VS Code Editor                         │
│  ┌────────────────────────────────────────────────────┐   │
│  │              VS Code Extension (TypeScript)         │   │
│  │  Tree View │ Flowchart │ Compare │ Inspector        │   │
│  └────────────────────────┬───────────────────────────┘   │
│                           │ MCP stdio                     │
│  ┌────────────────────────▼───────────────────────────┐   │
│  │         Python Core Engine (src/atomic_workflow/)   │   │
│  │  ┌────────┐ ┌──────────┐ ┌──────────┐ ┌─────────┐ │   │
│  │  │ Parser │ │ Resolver │ │Validator │ │  Graph  │ │   │
│  │  └────┬───┘ └────┬─────┘ └────┬─────┘ └────┬────┘ │   │
│  │       └──────────┼────────────┼─────────────┘      │   │
│  │                  ▼            ▼                     │   │
│  │  ┌─────────────────────┐ ┌───────────────────────┐ │   │
│  │  │   WorkflowService   │ │  WorkflowRepository   │ │   │
│  │  │     (§10.4)         │ │      (§12)            │ │   │
│  │  └─────────────────────┘ └───────────┬───────────┘ │   │
│  └──────────────────────────────────────┼─────────────┘   │
│                                         ▼                 │
│  ┌──────────────────────────────────────────────────────┐ │
│  │              Markdown Files (workflows/)              │ │
│  │  baseline/phase-a..l.md  │  variants/emergency.md     │ │
│  └──────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

## 核心模組

| 模組 | 職責 | SPEC |
|------|------|------|
| `domain/` | BaselineStep, VariantOverlay, ResolvedStep dataclasses | §1-3 |
| `parser/` | Markdown → 結構化物件 | §5-6 |
| `resolver/` | baseline + variant overlay → 最終步驟 | §7 |
| `validation/` | 規則驗證、ValidationReport | §8 |
| `graph/` | 步驟依賴圖產生 | §9 |
| `services/` | WorkflowService facade | §10.4 |
| `repository/` | DAL — 檔案讀寫 + snapshot | §12 |
| `mcp/` | MCP tool handlers (6 read + 17+ write) | §11 |

## Memory Bank (`memory-bank/`)

跨對話的專案記憶系統：

| 文件 | 用途 |
|------|------|
| `activeContext.md` | 當前工作焦點 |
| `progress.md` | 進度追蹤 |
| `decisionLog.md` | 決策記錄 |
| `productContext.md` | 專案上下文 |
| `projectBrief.md` | 專案簡介 |
| `systemPatterns.md` | 系統模式 |
| `architect.md` | 架構設計 |

## 三層演進

| Phase | Layer | 目標 |
|-------|-------|------|
| Phase 1 (MVP) | Redesign | VS Code 工作站：編輯 → 驗證 → 視覺化 → 討論 |
| Phase 2 | Dashboard | Streamlit 指標面板 |
| Phase 3 | Runtime Monitor | 即時追蹤執行 |

## 資料流

1. 用戶在 Chat 中輸入請求
2. Copilot 檢測是否匹配 Skill
3. 載入相關 Skill 定義
4. 結合 Memory Bank 上下文
5. 執行操作並更新文檔
