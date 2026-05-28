import React, { useCallback, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import WorkflowCanvas from '../components/WorkflowCanvas';
import NodePalette from '../components/NodePalette';
import NodeEditor from '../components/NodeEditor';
import EdgeEditor from '../components/EdgeEditor';
import { useWorkflows } from '../hooks/useWorkflow';
import { useExecution } from '../hooks/useExecution';
import { Play, Save } from 'lucide-react';

export default function WorkflowBuilderPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { currentWorkflow, fetchWorkflow, createWorkflow, editWorkflow } = useWorkflows();
  const { createExecution, startExecution } = useExecution();
  const [selectedNode, setSelectedNode] = React.useState(null);
  const [selectedEdge, setSelectedEdge] = React.useState(null);
  const [nodes, setNodes] = React.useState([]);
  const [edges, setEdges] = React.useState([]);
  const [name, setName] = React.useState('');
  const [description, setDescription] = React.useState('');

  useEffect(() => {
    if (id) {
      fetchWorkflow(id).then(w => {
        if (w) {
          setName(w.name);
          setDescription(w.description || '');
          setNodes(w.nodes?.map(n => ({
            id: n.id,
            type: 'default',
            position: n.position || { x: 200, y: 200 },
            data: { label: n.name || n.type, type: n.type, config: n.config || {} },
          })) || []);
          setEdges(w.edges?.map(e => ({
            id: e.id,
            source: e.source_id,
            target: e.target_id,
            label: e.label || '',
            type: e.type === 'conditional' ? 'step' : 'default',
          })) || []);
        }
      });
    }
  }, [id, fetchWorkflow]);

  const handleSave = async () => {
    const workflowData = {
      name,
      description,
      nodes: nodes.map(n => ({
        id: n.id,
        type: n.data.type,
        name: n.data.label,
        position: n.position,
        config: n.data.config || {},
      })),
      edges: edges.map(e => ({
        id: e.id || `edge_${Date.now()}`,
        source_id: e.source,
        target_id: e.target,
        label: e.label || '',
        type: e.type === 'step' ? 'conditional' : 'direct',
      })),
    };

    if (id) {
      await editWorkflow(id, workflowData);
    } else {
      const created = await createWorkflow(workflowData);
      if (created) navigate(`/workflows/${created.id}`, { replace: true });
    }
  };

  const handleRun = async () => {
    if (!id) return;
    const execution = await createExecution(id, {});
    if (execution) {
      await startExecution(execution.id, nodes, edges);
    }
  };

  const onNodesChangeHandler = useCallback((changes) => {
    setNodes(nds => {
      const updated = [...nds];
      for (const change of changes) {
        if (change.type === 'position' && change.dragging) {
          const idx = updated.findIndex(n => n.id === change.id);
          if (idx >= 0) updated[idx] = { ...updated[idx], position: change.position };
        }
        if (change.type === 'select') {
          setSelectedNode(change.selected ? updated.find(n => n.id === change.id) : null);
        }
        if (change.type === 'remove') {
          return updated.filter(n => n.id !== change.id);
        }
      }
      return updated;
    });
  }, []);

  const onEdgesChangeHandler = useCallback((changes) => {
    setEdges(eds => [...eds]);
  }, []);

  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-4 flex-1">
          <input value={name} onChange={e => setName(e.target.value)}
            placeholder="Workflow Name"
            className="bg-transparent text-xl font-bold text-white border-b border-slate-600 pb-1 focus:outline-none focus:border-blue-500" />
          <input value={description} onChange={e => setDescription(e.target.value)}
            placeholder="Description (optional)"
            className="bg-transparent text-sm text-slate-400 border-b border-slate-600 pb-1 focus:outline-none focus:border-blue-500 flex-1 max-w-md" />
        </div>
        <div className="flex items-center gap-2">
          <button onClick={handleSave}
            className="flex items-center gap-2 bg-slate-700 hover:bg-slate-600 text-white text-sm px-4 py-2 rounded">
            <Save size={16} /> Save
          </button>
          {id && (
            <button onClick={handleRun}
              className="flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white text-sm px-4 py-2 rounded">
              <Play size={16} /> Run
            </button>
          )}
        </div>
      </div>
      <div className="flex gap-4 flex-1 min-h-0">
        <div className="w-48 flex-shrink-0 overflow-y-auto">
          <NodePalette />
        </div>
        <div className="flex-1 bg-slate-900 rounded-lg border border-slate-700 overflow-hidden">
          <WorkflowCanvas
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChangeHandler}
            onEdgesChange={onEdgesChangeHandler}
          />
        </div>
        <div className="w-64 flex-shrink-0 overflow-y-auto space-y-4">
          <NodeEditor node={selectedNode} onSave={(n) => {
            setNodes(nds => nds.map(node => node.id === n.id ? n : node));
            setSelectedNode(null);
          }} onClose={() => setSelectedNode(null)} />
          <EdgeEditor edge={selectedEdge} onSave={(e) => {
            setEdges(eds => eds.map(edge => edge.id === e.id ? e : edge));
            setSelectedEdge(null);
          }} onClose={() => setSelectedEdge(null)} />
        </div>
      </div>
    </div>
  );
}
