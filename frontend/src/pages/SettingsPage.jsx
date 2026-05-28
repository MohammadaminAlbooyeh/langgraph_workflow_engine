import React from 'react';
import { Settings } from 'lucide-react';

export default function SettingsPage() {
  return (
    <div>
      <h2 className="text-2xl font-bold text-white mb-6">Settings</h2>
      <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
        <div className="space-y-4">
          {[
            { label: 'API Endpoint', value: process.env.REACT_APP_API_URL || '/api/v1' },
            { label: 'Environment', value: process.env.NODE_ENV || 'development' },
            { label: 'Version', value: '0.1.0' },
          ].map(s => (
            <div key={s.label} className="flex items-center justify-between py-2 border-b border-slate-700 last:border-0">
              <span className="text-sm text-slate-300">{s.label}</span>
              <span className="text-sm text-slate-500">{s.value}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
