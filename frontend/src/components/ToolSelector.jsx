import React, { useState } from 'react';
import { useTools } from '../hooks/useTools';
import { toolApi } from '../services/tool_api';

export default function ToolSelector() {
  const { tools, refetch } = useTools();
  const [selectedTool, setSelectedTool] = useState(null);
  const [result, setResult] = useState(null);
  const [params, setParams] = useState({});

  const handleExecute = async () => {
    if (!selectedTool) return;
    try {
      const { data } = await toolApi.execute(selectedTool.name, params);
      setResult(data);
    } catch (err) {
      setResult({ error: err.message });
    }
  };

  return (
    <div className="bg-slate-800 rounded-lg border border-slate-700 p-4">
      <h3 className="text-sm font-semibold text-slate-300 mb-4">Tool Selector</h3>
      <div className="space-y-3">
        <select
          value={selectedTool?.name || ''}
          onChange={e => {
            const tool = tools.find(t => t.name === e.target.value);
            setSelectedTool(tool);
            setParams({});
            setResult(null);
          }}
          className="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-sm text-white"
        >
          <option value="">Select a tool...</option>
          {tools.map(t => (
            <option key={t.name} value={t.name}>{t.name}</option>
          ))}
        </select>
        {selectedTool?.parameters?.map(param => (
          <div key={param.name}>
            <label className="text-xs text-slate-400 block mb-1">{param.name}</label>
            <input
              value={params[param.name] || ''}
              onChange={e => setParams({ ...params, [param.name]: e.target.value })}
              placeholder={param.description || ''}
              className="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-sm text-white"
            />
          </div>
        ))}
        {selectedTool && (
          <button onClick={handleExecute}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded py-2">
            Execute
          </button>
        )}
        {result && (
          <pre className="text-xs text-slate-300 bg-slate-900 p-3 rounded mt-2 overflow-auto max-h-32">
            {JSON.stringify(result, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
}
