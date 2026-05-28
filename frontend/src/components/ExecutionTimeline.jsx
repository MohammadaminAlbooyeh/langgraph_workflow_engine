import React from 'react';
import { formatDate } from '../utils/formatters';
import { constants } from '../utils/constants';

export default function ExecutionTimeline({ nodeResults = [] }) {
  if (!nodeResults?.length) {
    return <p className="text-slate-400 text-sm">No node results to display</p>;
  }

  return (
    <div className="space-y-2">
      {nodeResults.map((result, i) => (
        <div key={i} className="flex items-start gap-3 p-3 bg-slate-700/30 rounded border border-slate-700">
          <div className="w-2 h-2 rounded-full mt-1.5 flex-shrink-0"
            style={{ backgroundColor: constants.EXECUTION_STATUS_COLORS[result.status] || '#6b7280' }} />
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-white">{result.node_name || result.node_id}</span>
              <span className="text-xs text-slate-400">{formatDate(result.timestamp)}</span>
            </div>
            <p className="text-xs text-slate-400 capitalize mt-0.5">{result.status}</p>
            {result.error && <p className="text-xs text-red-400 mt-1">{result.error}</p>}
          </div>
        </div>
      ))}
    </div>
  );
}
