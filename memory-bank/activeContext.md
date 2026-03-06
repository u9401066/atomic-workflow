# Active Context

## Current Focus

BPMN-inspired extensions 完成，SPEC.md 更新至 ~3400+ 行。核心新增：
- §0.7 Concept Attribution（BPMN/FHIR/DMN/CMMN/SQL 概念溯源）
- §2.3 Shared Process Document（shared/ 目錄 + document_type: shared_process）
- §4.5.8 Node Type Classification（7 種 BPMN-inspired node types）
- §4.5.9 Step References / refs（7 種 relationship types，StepReference dataclass）
- §6 Domain Model 全面更新（StepReference + BaselineStep.node_type/refs + ResolvedStep.node_type/refs + WorkflowGraphNode.node_type/refs）
- §9 Graph schema 擴充（10 種 edge_type + 9.5 拓撲保證升級 + 9.6 Shared Process Subgraph Expansion）
- §13.5.2 React Flow 新增 4 node types + 7 edge types
- §13.6 TypeScript interfaces 全面更新（含 StepReferenceDTO）
- §18 Extensibility 大幅改寫：Decision/Cross-phase/Parallel/Shared 從 🟡🔴 升級至 ✅
- 下一步：開始實作 Python core engine

## Recently Changed Files

- `SPEC.md` — BPMN-inspired extensions（~15 處重大變更）
- `memory-bank/decisionLog.md` — 新增 BPMN cherry-pick 決策
- `memory-bank/progress.md` — 新增 BPMN extensions 完成項

## Current Blockers

- None