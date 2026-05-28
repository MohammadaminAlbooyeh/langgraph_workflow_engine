import React from 'react';

export default function EdgeEditor({ edge, onSave, onClose }) {
  const [label, setLabel] = React.useState(edge?.label || '');
  const [type, setType] = React.useState(edge?.type || 'direct');

  React.useEffect(() => {
    if (edge) {
      setLabel(edge.label || '');
      setType(edge.type || 'direct');
    }
  }, [edge]);

  if (!edge) {
    return (
      <div className="bg-slate-800 rounded-lg border border-slate-700 p-4">
        <p className="text-slate-400 text-sm">Select an edge to edit</p>
      </div>
    );
  }

  const handleSave = () => {
    onSave?.({ ...edge, label, type });
  };

  return (
    <div className="bg-slate-800 rounded-lg border border-slate-700 p-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-semibold text-slate-300">Edit Edge</h3>
        <button onClick={onClose} className="text-slate-400 hover:text-white text-xs">Close</button>
      </div>
      <div className="space-y-3">
        <div>
          <label className="text-xs text-slate-400 block mb-1">Label</label>
          <input value={label} onChange={e => setLabel(e.target.value)}
            className="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-sm text-white" />
        </div>
        <div>
          <label className="text-xs text-slate-400 block mb-1">Type</label>
          <select value={type} onChange={e => setType(e.target.value)}
            className="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-sm text-white">
            <option value="direct">Direct</option>
            <option value="conditional">Conditional</option>
            <option value="dynamic">Dynamic</option>
            <option value="event">Event</option>
          </select>
        </div>
        <button onClick={handleSave}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded py-2 transition-colors">
          Save
        </button>
      </div>
    </div>
  );
}
