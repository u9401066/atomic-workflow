import { useCallback, useMemo } from 'react';
import {
  ReactFlow,
  Controls,
  MiniMap,
  Background,
  BackgroundVariant,
  type NodeMouseHandler,
  type Node,
  type Edge,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

import StepNode from './nodes/StepNode';
import DecisionNode from './nodes/DecisionNode';
import { useWorkflowMessages } from './useWorkflowMessages';
import type { ReactFlowNodeData } from './types';

const nodeTypes = {
  step: StepNode,
  decision: DecisionNode,
  parallel: StepNode,
  subprocess: StepNode,
  event: StepNode,
  milestone: StepNode,
  narrative: StepNode,
};

const edgeStyles: Record<string, React.CSSProperties> = {
  sequential: { stroke: '#64748b', strokeWidth: 2 },
  variant_replace: { stroke: '#ef4444', strokeWidth: 2, strokeDasharray: '5 3' },
  variant_insert_after: { stroke: '#22c55e', strokeWidth: 2, strokeDasharray: '3 3' },
  triggers: { stroke: '#eab308', strokeWidth: 1.5, strokeDasharray: '5 3' },
  depends_on: { stroke: '#a855f7', strokeWidth: 1.5, strokeDasharray: '3 3' },
  parallel_with: { stroke: '#22c55e', strokeWidth: 2 },
  escalates_to: { stroke: '#ef4444', strokeWidth: 1.5, strokeDasharray: '5 3' },
};

function App() {
  const { graph, selectedStepId, onNodeClick } = useWorkflowMessages();

  const nodes: Node[] = useMemo(() => {
    if (!graph) { return []; }
    return graph.nodes.map((n) => ({
      id: n.id,
      type: n.type || 'step',
      position: n.position,
      data: n.data,
      selected: n.id === selectedStepId,
    }));
  }, [graph, selectedStepId]);

  const edges: Edge[] = useMemo(() => {
    if (!graph) { return []; }
    return graph.edges.map((e) => ({
      id: e.id,
      source: e.source,
      target: e.target,
      label: e.label,
      animated: e.animated ?? false,
      style: edgeStyles[e.type] ?? edgeStyles.sequential,
    }));
  }, [graph]);

  const handleNodeClick: NodeMouseHandler = useCallback(
    (_event, node) => {
      const data = node.data as ReactFlowNodeData;
      onNodeClick(data.stepId);
    },
    [onNodeClick],
  );

  if (!graph) {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        color: '#94a3b8',
        fontFamily: 'system-ui, sans-serif',
      }}>
        Loading workflow graph…
      </div>
    );
  }

  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <div style={{
        padding: '8px 16px',
        borderBottom: '1px solid #334155',
        backgroundColor: '#0f172a',
        color: '#e2e8f0',
        fontFamily: 'system-ui, sans-serif',
        fontSize: 13,
        display: 'flex',
        gap: 16,
        alignItems: 'center',
      }}>
        <strong>Phase {graph.meta.phase}</strong>
        <span style={{ color: '#94a3b8' }}>
          {graph.meta.variant} · {graph.meta.nodeCount} steps · {graph.meta.edgeCount} edges
        </span>
      </div>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        onNodeClick={handleNodeClick}
        fitView
        minZoom={0.2}
        maxZoom={2}
        defaultEdgeOptions={{ type: 'smoothstep' }}
        style={{ backgroundColor: '#0f172a' }}
      >
        <Controls position="bottom-left" />
        <MiniMap
          nodeStrokeWidth={3}
          pannable
          zoomable
          style={{ backgroundColor: '#1e293b' }}
        />
        <Background variant={BackgroundVariant.Dots} gap={16} size={1} color="#1e293b" />
      </ReactFlow>
    </div>
  );
}

export default App;
