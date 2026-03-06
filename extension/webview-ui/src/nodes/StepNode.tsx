import { memo } from 'react';
import { Handle, Position } from '@xyflow/react';
import type { ReactFlowNodeData } from '../types';

const KIND_COLORS: Record<string, string> = {
  baseline: '#3b82f6',
  modified: '#f97316',
  variant_only: '#ef4444',
  replacement: '#ef4444',
  skipped: '#9ca3af',
  narrative: '#d1d5db',
};

interface StepNodeProps {
  data: ReactFlowNodeData;
  selected: boolean;
}

function StepNode({ data, selected }: StepNodeProps) {
  const borderColor = KIND_COLORS[data.kind] ?? '#3b82f6';

  return (
    <div
      style={{
        padding: '8px 12px',
        borderRadius: 8,
        border: `2px solid ${borderColor}`,
        backgroundColor: selected ? '#1e293b' : '#0f172a',
        color: '#e2e8f0',
        minWidth: 160,
        maxWidth: 280,
        fontSize: 12,
        boxShadow: selected ? `0 0 0 2px ${borderColor}` : 'none',
        opacity: data.kind === 'skipped' ? 0.5 : 1,
      }}
    >
      <Handle type="target" position={Position.Top} style={{ background: borderColor }} />
      <div style={{ fontWeight: 600, marginBottom: 4, fontSize: 11, color: '#94a3b8' }}>
        {data.stepId}
      </div>
      <div style={{ fontWeight: 500 }}>{data.label}</div>
      {data.kind !== 'baseline' && (
        <div
          style={{
            marginTop: 4,
            fontSize: 10,
            padding: '1px 6px',
            borderRadius: 4,
            backgroundColor: borderColor + '33',
            color: borderColor,
            display: 'inline-block',
          }}
        >
          {data.kind}
        </div>
      )}
      <Handle type="source" position={Position.Bottom} style={{ background: borderColor }} />
    </div>
  );
}

export default memo(StepNode);
