import React from 'react';
import { constants } from '../utils/constants';
import { formatDuration, formatDate } from '../utils/formatters';

export default function ExecutionMonitor({ execution }) {
  if (!execution) {
    return (
      <div className="bg-slate-800 rounded-lg border border-slate-700 p-4">
        <p className="text-slate-400 text-sm">No execution selected</p>
      </div>
    );
  }

  const statusColor = constants.EXECUTION_STATUS_COLORS[execution.status] || '#6b7280';

  return (
    <div className="bg-slate-800 rounded-lg border border-slate-700 p-4">
      <h3 className="text-sm font-semibold text-slate-300 mb-4">Execution Monitor</h3>
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-xs text-slate-400">Status</span>
          <span className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full" style={{ backgroundColor: statusColor }} />
            <span className="text-sm text-white capitalize">{execution.status}</span>
          </span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-xs text-slate-400">Duration</span>
          <span className="text-sm text-white">{formatDuration(execution.duration_ms)}</span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-xs text-slate-400">Started</span>
          <span className="text-sm text-white">{formatDate(execution.started_at)}</span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-xs text-slate-400">Completed</span>
          <span className="text-sm text-white">{formatDate(execution.completed_at)}</span>
        </div>
        {execution.error && (
          <div className="mt-2 p-2 bg-red-900/30 border border-red-800 rounded">
            <p className="text-xs text-red-400">{execution.error}</p>
          </div>
        )}
      </div>
    </div>
  );
}
