# 子法：架構規範 — Atomic Workflow

> 父法：CONSTITUTION.md 第一章

## 第 1 條：目錄結構

```
src/atomic_workflow/
├── domain/                    # 領域層（核心 dataclasses，無外部依賴）
│   ├── models.py              # BaselineStep, VariantOverlay, ResolvedStep
│   ├── enums.py               # Phase, Role, Equipment 等列舉
│   └── errors.py              # 領域層例外
│
├── parser/                    # 解析器
│   ├── baseline_parser.py     # Baseline markdown → BaselineStep (§5)
│   └── variant_parser.py      # Variant markdown → VariantOverlay (§6)
│
├── resolver/                  # Variant 疊加解析
│   └── variant_resolver.py    # baseline + overlay → ResolvedStep (§7)
│
├── validation/                # 驗證引擎
│   └── validator.py           # ValidationReport builder (§8)
│
├── graph/                     # 圖形產生
│   └── graph_generator.py     # 步驟依賴圖 → Mermaid/JSON (§9)
│
├── services/                  # 應用層 Facade
│   └── workflow_service.py    # WorkflowService (§10.4)
│
├── repository/                # DAL 資料存取
│   └── workflow_repository.py # 檔案系統讀寫 + snapshot (§12)
│
└── mcp/                       # MCP 工具介面
    └── tools.py               # MCP tool handlers (§11)
```

## 第 2 條：依賴方向

```
VS Code Extension → (MCP stdio) → Python Core Engine → Markdown Files

Python 內部：
  services/ → parser/ + resolver/ + validation/ + graph/
                              ↓
                     domain/ + repository/
```

- domain/ 不依賴任何其他模組（僅用 Python 標準庫 + dataclasses）
- repository/ 封裝所有檔案系統操作
- services/ 是唯一的外部入口（MCP 呼叫 services/）

## 第 3 條：DAL 規範

### 3.1 Repository 實作（在 repository/ 層）

Repository 負責所有 Markdown 檔案的讀寫操作：

```python
# repository/workflow_repository.py
class WorkflowRepository:
    def __init__(self, workflows_dir: Path) -> None:
        self._root = workflows_dir

    def load_baseline_file(self, path: Path) -> str:
        """讀取 baseline markdown 原始內容"""
        ...

    def save_step(self, path: Path, content: str) -> WriteResult:
        """寫回修改後的 step，回傳 WriteResult 信封"""
        ...

    def create_snapshot(self) -> str:
        """建立快照供回滾使用"""
        ...
```

### 3.2 WriteResult 信封

所有寫入操作必須回傳 WriteResult：

```python
@dataclass(frozen=True)
class WriteResult:
    success: bool
    path: Path
    snapshot_id: str | None
    message: str
```

## 第 4 條：命名慣例

| 類型 | 命名規則 | 範例 |
|------|----------|------|
| Dataclass | 名詞單數 | `BaselineStep`, `ResolvedStep` |
| Enum | 名詞 | `Phase`, `Role`, `Equipment` |
| Parser | `{target}_parser` | `baseline_parser`, `variant_parser` |
| Service | `{domain}_service` | `workflow_service` |
| Repository | `{domain}_repository` | `workflow_repository` |
| Domain Event | 過去式 | `OrderCreated`, `UserRegistered` |

---

## 第 5 條：模組化規範

> 依據憲法第 7.3 條「主動重構原則」訂定

### 5.1 檔案長度限制

| 類型 | 建議上限 | 硬性上限 | 超過時動作 |
|------|----------|----------|------------|
| 單一檔案 | 200 行 | 400 行 | 必須拆分 |
| 類別 (Class) | 150 行 | 300 行 | 提取子類別或組合 |
| 函數 (Function) | 30 行 | 50 行 | 提取私有方法 |
| 模組 (目錄) | 10 檔案 | 15 檔案 | 建立子模組 |

### 5.2 複雜度指標

```python
# 圈複雜度 (Cyclomatic Complexity)
# 建議 ≤ 10，硬性上限 15

# ❌ 過於複雜
def process_order(order):
    if order.status == "pending":
        if order.payment:
            if order.payment.verified:
                if order.items:
                    for item in order.items:
                        if item.in_stock:
                            # ... 更多巢狀
                            
# ✅ 重構後
def process_order(order):
    validate_order_status(order)
    verify_payment(order.payment)
    process_items(order.items)
```

### 5.3 模組拆分策略

當 Domain 模組過大時，按 **子領域** 拆分：

```
# Before: 單一 Domain
src/Domain/
├── Entities/
│   ├── User.py
│   ├── Order.py
│   ├── Product.py
│   ├── Payment.py
│   └── Shipping.py  # 太多了！

# After: 按子領域拆分
src/Domain/
├── Identity/           # 身份子領域
│   ├── Entities/
│   │   └── User.py
│   └── ValueObjects/
│       └── Email.py
│
├── Ordering/           # 訂單子領域
│   ├── Entities/
│   │   └── Order.py
│   ├── ValueObjects/
│   │   └── OrderStatus.py
│   └── DomainServices/
│       └── OrderPricing.py
│
├── Catalog/            # 商品目錄子領域
│   └── Entities/
│       └── Product.py
│
└── Shipping/           # 物流子領域
    └── Entities/
        └── Shipment.py
```

### 5.4 Application 層拆分

按 **功能群組** 或 **用例** 拆分：

```
src/Application/
├── Identity/           # 對應 Domain/Identity
│   ├── Commands/
│   │   ├── RegisterUser.py
│   │   └── ChangePassword.py
│   └── Queries/
│       └── GetUserProfile.py
│
├── Ordering/           # 對應 Domain/Ordering
│   ├── Commands/
│   │   ├── CreateOrder.py
│   │   └── CancelOrder.py
│   └── Queries/
│       └── GetOrderHistory.py
```

### 5.5 重構觸發條件

AI 應在以下情況 **主動建議** 重構：

| 觸發條件 | 建議動作 |
|----------|----------|
| 檔案超過 200 行 | 「這個檔案有點長，建議拆分成...」 |
| 函數超過 30 行 | 「這個函數可以提取出...」 |
| 圈複雜度 > 10 | 「這段邏輯較複雜，建議...」 |
| 重複程式碼 | 「發現重複模式，建議抽取為...」 |
| 跨層依賴 | 「這裡違反了 DDD 分層，應該...」 |

---

## 第 6 條：重構安全網

### 6.1 重構前必須

1. ✅ 確保有測試覆蓋（覆蓋率 ≥ 70%）
2. ✅ 執行現有測試確認通過
3. ✅ 記錄重構原因到 `decisionLog.md`

### 6.2 重構後必須

1. ✅ 執行全部測試
2. ✅ 檢查架構是否仍符合 DDD
3. ✅ 更新相關文檔
4. ✅ 更新 `memory-bank/architect.md`

### 6.3 重構模式參考

| 問題 | 重構模式 | 說明 |
|------|----------|------|
| 函數過長 | Extract Method | 提取私有方法 |
| 類別過大 | Extract Class | 提取新類別 |
| 重複程式碼 | Extract Superclass / Trait | 抽取共用邏輯 |
| 過多參數 | Introduce Parameter Object | 建立參數物件 |
| 條件過複雜 | Replace Conditional with Polymorphism | 用多態取代條件 |
| 跨層依賴 | Dependency Injection | 依賴注入 |
