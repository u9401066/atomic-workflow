import { memo } from 'react';
import { Handle, Position } from '@xyflow/react';
import type { ReactFlowNodeData } from '../types';

interface DecisionNodeProps {
  data: ReactFlowNodeData;
  selected: boolean;
}

function DecisionNode({ data, selected }: DecisionNodeProps) {
  return (
    <div
      style={{
        width: 120,
        height: 80,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative',
      }}
    >
      <Handle type="target" position={Position.Top} style={{ background: '#eab308' }} />
      <div
        style={{
          width: '100%',
          height: '100%',
          transform: 'rotate(45deg)',
          backgroundColor: selected ? '#854d0e' : '#713f12',
          border: `2px solid ${selected ? '#facc15' : '#eab308'}`,
          borderRadius: 4,
          position: 'absolute',
        }}
      />
      <div
        style={{
          position: 'relative',
          zIndex: 1,
          color: '#fef9c3',
          fontSize: 10,
          fontWeight: 600,
          textAlign: 'center',
          maxWidth: 90,
          lineHeight: '1.2',
        }}
      >
        {data.label}
      </div>
      <Handle type="source" position={Position.Bottom} style={{ background: '#eab308' }} />
    </div>
  );
}

export default memo(DecisionNode);
