import React from 'react';
import { Bot } from 'lucide-react';
import { useAgents } from '../hooks/useAgent';

export default function AgentManager() {
  const { agents, loading } = useAgents();

  return (
    <div className="bg-slate-800 rounded-lg border border-slate-700 p-4">
      <h3 className="text-sm font-semibold text-slate-300 mb-4">Agents</h3>
      {loading ? (
        <p className="text-slate-400 text-sm">Loading...</p>
      ) : agents.length === 0 ? (
        <p className="text-slate-400 text-sm">No agents configured</p>
      ) : (
        <div className="space-y-2">
          {agents.map(agent => (
            <div key={agent.id} className="flex items-center gap-3 p-3 bg-slate-700/30 rounded border border-slate-700">
              <Bot size={18} className="text-blue-400" />
              <div>
                <p className="text-sm text-white">{agent.name}</p>
                <p className="text-xs text-slate-400">{agent.config?.model || agent.config?.provider}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
