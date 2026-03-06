# 專案憲法 (Project Constitution) — Atomic Workflow

本文件定義 Atomic Workflow 專案的最高原則，所有 Agents、程式碼和規格文件必須遵守。

---

## 第一章：架構原則

### 第 1 條：結構化檔案為唯一資料來源
1. 臨床工作流程以結構化 Markdown 檔案儲存，**不使用資料庫**（SPEC §0.4）
2. baseline + variant overlay 為唯一工作流程表述模式
3. 檔案即原始碼：可 git diff、可 PR review、可 AI 存取

### 第 2 條：SPEC.md 為唯一實作契約
1. `SPEC.md` 是完整的技術規格，修改程式碼前先更新規格
2. 程式碼是規格的「編譯產物」
3. 規格與程式碼衝突時，以規格為準（修正程式碼）

### 第 3 條：分層架構（Python Core Engine）
```
src/atomic_workflow/
├── domain/       # 核心領域（dataclasses，無外部依賴）
├── parser/       # baseline + variant 解析器
├── resolver/     # variant overlay 解析
├── validation/   # 規則驗證
├── graph/        # 圖形產生
├── services/     # WorkflowService facade
├── repository/   # WorkflowRepository（DAL）
└── mcp/          # MCP tool handlers
```

### 第 4 條：DAL 資料存取層獨立
1. Repository Pattern 為唯一資料存取方式
2. 禁止在 domain/ 直接操作檔案系統
3. 所有寫入操作必須透過 WriteResult 信封回傳

### 第 5 條：依賴方向
1. VS Code Extension → (MCP stdio) → Python Core Engine → Markdown Files
2. Python 內部：`services/ → parser/ + resolver/ + validation/ + graph/ → domain/ + repository/`
3. domain/ 不可依賴其他模組

---

## 第二章：Memory Bank 原則

### 第 6 條：操作綁定
1. 每次重要操作必須同步更新 Memory Bank
2. Memory Bank 是專案的「長期記憶」
3. 優先更新順序：progress > activeContext > decisionLog

> **「想要寫文件的時候，就更新 Memory Bank 吧！」**
>
> 不要另開文件寫筆記，直接寫進 Memory Bank，讓知識留在專案內。

### 第 7 條：更新時機
| 操作類型 | 必須更新 |
|----------|----------|
| 完成功能 | progress.md (Done) |
| 開始任務 | progress.md (Doing), activeContext.md |
| 重大決策 | decisionLog.md |
| 架構變更 | architect.md, systemPatterns.md |

---

## 第三章：文檔與測試原則

### 第 8 條：文檔優先
1. 程式碼是文檔的「編譯產物」
2. 修改程式碼前先更新 SPEC.md
3. README 是專案的「門面」，必須保持最新

### 第 9 條：測試即文檔
1. 測試程式碼是最好的使用範例
2. 零散測試也是測試，寫進 `tests/` 資料夾
3. 不要在 REPL 或 notebook 中測試後就丟棄

> **「想要零散測試的時候，就寫測試檔案進 tests/ 資料夾吧！」**
>
> 今天的零散測試，就是明天的回歸測試。

### 第 10 條：環境即程式碼
1. 使用 uv 管理 Python 環境和依賴
2. 依賴必須在 pyproject.toml + uv.lock 中鎖定
3. 環境設定納入版本控制

---

## 第四章：子法授權

### 第 11 條：子法層級
```
憲法 (CONSTITUTION.md)  ← 最高原則
  ├── 子法 (.github/bylaws/*.md)  ← 細則規範
  └── 規格 (SPEC.md)  ← 技術實作契約
```

### 第 12 條：子法優先順序
1. 子法不得違反憲法
2. 衝突時以較高層級為準
3. 未規範事項由各模組自行決定

---

## 附則

### 第 13 條：修憲程序
1. 修改憲法須在 decisionLog.md 記錄原因
2. 重大修改須更新版本號
3. 本憲法版本：v1.0.0
