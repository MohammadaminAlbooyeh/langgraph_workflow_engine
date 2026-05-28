import React from 'react';
import { useWorkflows } from '../hooks/useWorkflow';
import { formatDate } from '../utils/formatters';
import { History } from 'lucide-react';

export default function HistoryPage() {
  const { workflows } = useWorkflows();

  const allExecutions = workflows.flatMap(w =>
    (w.executions || []).map(ex => ({ ...ex, workflow_name: w.name }))
  ).sort((a, b) => new Date(b.started_at) - new Date(a.started_at));

  return (
    <div>
      <h2 className="text-2xl font-bold text-white mb-6">History</h2>
      {allExecutions.length === 0 ? (
        <div className="bg-slate-800 rounded-lg border border-slate-700 p-12 text-center">
          <History size={48} className="text-slate-600 mx-auto mb-4" />
          <p className="text-slate-400">No execution history yet.</p>
        </div>
      ) : (
        <div className="bg-slate-800 rounded-lg border border-slate-700">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-700 text-slate-400">
                <th className="text-left p-4">Workflow</th>
                <th className="text-left p-4">Status</th>
                <th className="text-left p-4">Started</th>
                <th className="text-right p-4">Duration</th>
              </tr>
            </thead>
            <tbody>
              {allExecutions.map((ex, i) => (
                <tr key={i} className="border-b border-slate-700/50 text-slate-300">
                  <td className="p-4">{ex.workflow_name}</td>
                  <td className="p-4 capitalize">{ex.status}</td>
                  <td className="p-4">{formatDate(ex.started_at)}</td>
                  <td className="p-4 text-right">{Math.round(ex.duration_ms || 0)}ms</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
