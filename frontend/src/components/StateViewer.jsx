import React from 'react';

export default function StateViewer({ state }) {
  if (!state || !Object.keys(state).length) {
    return <p className="text-slate-400 text-sm">No state data</p>;
  }

  return (
    <div className="bg-slate-800 rounded-lg border border-slate-700 p-4">
      <h3 className="text-sm font-semibold text-slate-300 mb-3">State</h3>
      <pre className="text-xs text-slate-300 overflow-auto max-h-60 bg-slate-900 p-3 rounded">
        {JSON.stringify(state, null, 2)}
      </pre>
    </div>
  );
}
