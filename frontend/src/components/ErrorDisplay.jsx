import React from 'react';
import { AlertTriangle, X } from 'lucide-react';

export default function ErrorDisplay({ error, onDismiss }) {
  if (!error) return null;

  return (
    <div className="bg-red-900/30 border border-red-800 rounded-lg p-4 flex items-start gap-3">
      <AlertTriangle size={18} className="text-red-400 mt-0.5 flex-shrink-0" />
      <p className="text-sm text-red-300 flex-1">{error}</p>
      {onDismiss && (
        <button onClick={onDismiss} className="text-red-400 hover:text-red-300 flex-shrink-0">
          <X size={16} />
        </button>
      )}
    </div>
  );
}
