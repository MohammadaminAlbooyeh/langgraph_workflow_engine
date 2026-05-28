import React from 'react';
import { useMonitoring } from '../hooks/useMonitoring';
import { BarChart3, Activity, CheckCircle, AlertTriangle } from 'lucide-react';

export default function MonitoringPage() {
  const { summary } = useMonitoring();

  const metrics = [
    { label: 'Total Executions', value: summary?.total_executions || 0, icon: BarChart3, color: 'text-blue-400' },
    { label: 'Total Errors', value: summary?.total_errors || 0, icon: AlertTriangle, color: 'text-red-400' },
  ];

  return (
    <div>
      <h2 className="text-2xl font-bold text-white mb-6">Monitoring</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        {metrics.map(m => (
          <div key={m.label} className="bg-slate-800 rounded-lg border border-slate-700 p-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-400">{m.label}</span>
              <m.icon size={20} className={m.color} />
            </div>
            <p className="text-3xl font-bold text-white mt-2">{m.value}</p>
          </div>
        ))}
      </div>
      <div className="bg-slate-800 rounded-lg border border-slate-700 p-4">
        <h3 className="text-sm font-semibold text-slate-300 mb-3">Recent Executions</h3>
        {summary?.recent_executions?.length > 0 ? (
          <div className="space-y-2">
            {summary.recent_executions.map((ex, i) => (
              <div key={i} className="flex items-center justify-between py-2 border-b border-slate-700 last:border-0">
                <span className="text-sm text-slate-300">{ex.workflow_id}</span>
                <div className="flex items-center gap-3">
                  <span className="text-xs text-slate-400">{Math.round(ex.duration_ms)}ms</span>
                  <span className={`text-xs capitalize ${
                    ex.status === 'completed' ? 'text-green-400' : ex.status === 'failed' ? 'text-red-400' : 'text-blue-400'
                  }`}>{ex.status}</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-slate-400 text-sm">No executions recorded yet</p>
        )}
      </div>
    </div>
  );
}
