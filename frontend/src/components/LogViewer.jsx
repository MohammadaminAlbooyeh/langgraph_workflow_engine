import React from 'react';

export default function LogViewer({ logs = [] }) {
  return (
    <div className="bg-slate-900 rounded-lg border border-slate-700 p-4">
      <h3 className="text-sm font-semibold text-slate-300 mb-3">Logs</h3>
      <div className="h-48 overflow-auto font-mono text-xs space-y-1">
        {logs.length === 0 && <p className="text-slate-500">No logs yet</p>}
        {logs.map((log, i) => (
          <div key={i} className="text-slate-400">
            <span className="text-slate-600">{log.timestamp || '[--:--:--]'}</span>{' '}
            <span className={log.level === 'error' ? 'text-red-400' : log.level === 'warn' ? 'text-yellow-400' : 'text-slate-300'}>
              {log.message}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
