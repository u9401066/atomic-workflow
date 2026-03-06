/** Shared types mirroring messages.ts from extension host */

export interface ReactFlowNodeData {
  label: string;
  stepId: string;
  phase: string;
  variant: string;
  kind: string;
  nodeType: string;
  refs: Array<{ target: string; type: string; condition?: string; description?: string }>;
}

export interface GraphPayload {
  nodes: Array<{
    id: string;
    type: string;
    position: { x: number; y: number };
    data: ReactFlowNodeData;
  }>;
  edges: Array<{
    id: string;
    source: string;
    target: string;
    type: string;
    label?: string;
    animated?: boolean;
    data?: { description?: string };
  }>;
  meta: { phase: string; variant: string; nodeCount: number; edgeCount: number };
}
