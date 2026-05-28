import React from 'react';
import ToolSelector from '../components/ToolSelector';
import { useTools } from '../hooks/useTools';

export default function ToolsPage() {
  const { tools } = useTools();

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div className="lg:col-span-2">
        <h2 className="text-2xl font-bold text-white mb-6">Tools</h2>
        {tools.length === 0 ? (
          <div className="bg-slate-800 rounded-lg border border-slate-700 p-12 text-center">
            <p className="text-slate-400">No tools registered.</p>
          </div>
        ) : (
          <div className="grid gap-3">
            {tools.map(tool => (
              <div key={tool.name} className="bg-slate-800 rounded-lg border border-slate-700 p-4">
                <p className="text-white font-medium">{tool.name}</p>
                <p className="text-xs text-slate-400 mt-1">{tool.description || 'No description'}</p>
              </div>
            ))}
          </div>
        )}
      </div>
      <div>
        <ToolSelector />
      </div>
    </div>
  );
}
