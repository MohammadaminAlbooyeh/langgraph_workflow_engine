import { constants } from './constants';

export const createGraphFromWorkflow = (workflow) => {
  if (!workflow) return { nodes: [], edges: [] };

  const nodes = (workflow.nodes || []).map(n => ({
    id: n.id,
    type: 'default',
    position: n.position || { x: Math.random() * 400, y: Math.random() * 400 },
    data: {
      label: n.name || n.type,
      type: n.type,
      color: constants.NODE_COLORS[n.type] || '#6b7280',
      config: n.config,
    },
  }));

  const edges = (workflow.edges || []).map(e => ({
    id: e.id,
    source: e.source_id,
    target: e.target_id,
    label: e.label || '',
    animated: e.type === 'dynamic' || e.type === 'event',
    style: { stroke: e.type === 'conditional' ? '#f59e0b' : '#64748b' },
  }));

  return { nodes, edges };
};
