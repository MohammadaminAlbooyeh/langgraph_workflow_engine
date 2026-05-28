import React from 'react';
import AgentManager from '../components/AgentManager';

export default function AgentsPage() {
  return (
    <div>
      <h2 className="text-2xl font-bold text-white mb-6">Agents</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <AgentManager />
      </div>
    </div>
  );
}
