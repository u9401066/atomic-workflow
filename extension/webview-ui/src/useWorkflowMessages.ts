import { useCallback, useEffect, useState } from 'react';
import type { GraphPayload } from './types';
import { getVsCodeApi, postMessage } from './hooks/useVsCodeApi';

type Message =
  | { type: 'graph:update'; payload: GraphPayload }
  | { type: 'step:select'; payload: { stepId: string } }
  | { type: 'variant:changed'; payload: { variant: string } }
  | { type: 'theme:changed'; payload: { isDark: boolean } };

export function useWorkflowMessages() {
  const [graph, setGraph] = useState<GraphPayload | null>(null);
  const [selectedStepId, setSelectedStepId] = useState<string | null>(null);

  useEffect(() => {
    const handler = (event: MessageEvent<Message>) => {
      const msg = event.data;
      switch (msg.type) {
        case 'graph:update':
          setGraph(msg.payload);
          break;
        case 'step:select':
          setSelectedStepId(msg.payload.stepId);
          break;
      }
    };
    window.addEventListener('message', handler);

    // Signal ready to extension host
    postMessage({ type: 'ready' });

    return () => window.removeEventListener('message', handler);
  }, []);

  const onNodeClick = useCallback((stepId: string) => {
    setSelectedStepId(stepId);
    postMessage({ type: 'node:clicked', payload: { stepId } });
  }, []);

  return { graph, selectedStepId, onNodeClick };
}
