// Shared message types for extension host ↔ webview communication

export interface ReactFlowNodeData {
  label: string;
  stepId: string;
  phase: string;
  variant: string;
  kind: string;
  nodeType: string;
  refs: Array<{ target: string; type: string; condition?: string; description?: string }>;
}

export interface ReactFlowNode {
  id: string;
  type: string;
  position: { x: number; y: number };
  data: ReactFlowNodeData;
}

export interface ReactFlowEdge {
  id: string;
  source: string;
  target: string;
  type: string;
  label?: string;
  animated?: boolean;
  data?: { description?: string };
}

export interface GraphPayload {
  nodes: ReactFlowNode[];
  edges: ReactFlowEdge[];
  meta: { phase: string; variant: string; nodeCount: number; edgeCount: number };
}

export interface ValidationIssue {
  severity: 'error' | 'warning' | 'info';
  code: string;
  message: string;
  file: string;
  line?: number;
  step_id?: string;
}

// Extension Host → Webview
export type ExtToWebview =
  | { type: 'graph:update'; payload: GraphPayload }
  | { type: 'step:select'; payload: { stepId: string } }
  | { type: 'variant:changed'; payload: { variant: string } }
  | { type: 'validation:results'; payload: ValidationIssue[] }
  | { type: 'theme:changed'; payload: { isDark: boolean } };

// Webview → Extension Host
export type WebviewToExt =
  | { type: 'node:clicked'; payload: { stepId: string } }
  | { type: 'node:moved'; payload: { stepId: string; position: { x: number; y: number } } }
  | { type: 'variant:select'; payload: { variant: string } }
  | { type: 'command:execute'; payload: { command: string; args: unknown[] } }
  | { type: 'ready' };
