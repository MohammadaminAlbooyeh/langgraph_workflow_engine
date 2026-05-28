import React from 'react';
import { Link } from 'react-router-dom';
import { useWorkflows } from '../hooks/useWorkflow';
import { Plus, Edit, Trash2, Workflow } from 'lucide-react';
import { formatDate } from '../utils/formatters';

export default function WorkflowsPage() {
  const { workflows, removeWorkflow } = useWorkflows();

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-white">Workflows</h2>
        <Link to="/workflows/new"
          className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-4 py-2 rounded transition-colors">
          <Plus size={16} /> New Workflow
        </Link>
      </div>
      {workflows.length === 0 ? (
        <div className="bg-slate-800 rounded-lg border border-slate-700 p-12 text-center">
          <Workflow size={48} className="text-slate-600 mx-auto mb-4" />
          <p className="text-slate-400 mb-4">No workflows yet. Create your first one!</p>
          <Link to="/workflows/new"
            className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded text-sm">
            <Plus size={16} /> Create Workflow
          </Link>
        </div>
      ) : (
        <div className="grid gap-4">
          {workflows.map(w => (
            <div key={w.id} className="bg-slate-800 rounded-lg border border-slate-700 p-4 flex items-center justify-between">
              <div>
                <Link to={`/workflows/${w.id}`} className="text-white font-medium hover:text-blue-400 transition-colors">{w.name}</Link>
                <div className="flex items-center gap-3 mt-1">
                  <span className="text-xs bg-slate-700 text-slate-300 px-2 py-0.5 rounded capitalize">{w.type}</span>
                  <span className="text-xs text-slate-500">{w.nodes?.length || 0} nodes</span>
                  <span className="text-xs text-slate-500">{formatDate(w.updated_at)}</span>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Link to={`/workflows/${w.id}`}
                  className="text-slate-400 hover:text-white p-1.5 rounded hover:bg-slate-700">
                  <Edit size={16} />
                </Link>
                <button onClick={() => removeWorkflow(w.id)}
                  className="text-slate-400 hover:text-red-400 p-1.5 rounded hover:bg-slate-700">
                  <Trash2 size={16} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
