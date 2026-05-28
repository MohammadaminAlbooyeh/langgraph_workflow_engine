import React, { useState, useEffect } from 'react';

export default function NodeEditor({ node, onSave, onClose }) {
  const [config, setConfig] = useState(node?.config || {});
  const [name, setName] = useState(node?.data?.label || '');

  useEffect(() => {
    if (node) {
      setName(node.data?.label || '');
      setConfig(node.config || {});
    }
  }, [node]);

  if (!node) {
    return (
      <div className="bg-slate-800 rounded-lg border border-slate-700 p-4">
        <p className="text-slate-400 text-sm">Select a node to edit</p>
      </div>
    );
  }

  const handleSave = () => {
    onSave?.({ ...node, data: { ...node.data, label: name }, config });
  };

  return (
    <div className="bg-slate-800 rounded-lg border border-slate-700 p-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-semibold text-slate-300">Edit Node</h3>
        <button onClick={onClose} className="text-slate-400 hover:text-white text-xs">Close</button>
      </div>
      <div className="space-y-3">
        <div>
          <label className="text-xs text-slate-400 block mb-1">Name</label>
          <input
            value={name}
            onChange={e => setName(e.target.value)}
            className="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-sm text-white"
          />
        </div>
        <div>
          <label className="text-xs text-slate-400 block mb-1">Type</label>
          <input value={node.data?.type || ''} disabled className="w-full bg-slate-700/50 border border-slate-600 rounded px-3 py-2 text-sm text-slate-400" />
        </div>
        {node.data?.type === 'llm' && (
          <>
            <div>
              <label className="text-xs text-slate-400 block mb-1">Temperature</label>
              <input type="number" step="0.1" min="0" max="2"
                value={config.temperature ?? 0.7}
                onChange={e => setConfig({ ...config, temperature: parseFloat(e.target.value) })}
                className="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-sm text-white" />
            </div>
            <div>
              <label className="text-xs text-slate-400 block mb-1">Max Tokens</label>
              <input type="number"
                value={config.maxTokens ?? 4096}
                onChange={e => setConfig({ ...config, maxTokens: parseInt(e.target.value) })}
                className="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-sm text-white" />
            </div>
          </>
        )}
        {node.data?.type === 'conditional' && (
          <div>
            <label className="text-xs text-slate-400 block mb-1">Condition Field</label>
            <input value={config.conditionField || ''}
              onChange={e => setConfig({ ...config, conditionField: e.target.value })}
              className="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-sm text-white" />
          </div>
        )}
        <button onClick={handleSave}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded py-2 transition-colors">
          Save
        </button>
      </div>
    </div>
  );
}
