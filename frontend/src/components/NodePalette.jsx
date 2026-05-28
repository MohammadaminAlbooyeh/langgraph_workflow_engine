import React from 'react';
import { handleDragStart } from '../utils/drag_drop';
import { constants } from '../utils/constants';

const nodeCategories = [
  {
    label: 'Agents',
    items: [
      { type: 'agent', label: 'Agent', color: '#3b82f6' },
      { type: 'llm', label: 'LLM', color: '#8b5cf6' },
    ],
  },
  {
    label: 'Input / Output',
    items: [
      { type: 'input', label: 'Input', color: '#10b981' },
      { type: 'output', label: 'Output', color: '#f59e0b' },
    ],
  },
  {
    label: 'Decision',
    items: [
      { type: 'conditional', label: 'Conditional', color: '#ef4444' },
      { type: 'router', label: 'Router', color: '#f97316' },
      { type: 'loop', label: 'Loop', color: '#f97316' },
    ],
  },
  {
    label: 'Processing',
    items: [
      { type: 'transformer', label: 'Transformer', color: '#06b6d4' },
      { type: 'validator', label: 'Validator', color: '#84cc16' },
      { type: 'text_processor', label: 'Text', color: '#14b8a6' },
      { type: 'custom', label: 'Custom', color: '#6b7280' },
    ],
  },
  {
    label: 'Aggregation',
    items: [
      { type: 'aggregate', label: 'Aggregate', color: '#ec4899' },
      { type: 'merge', label: 'Merge', color: '#a855f7' },
      { type: 'combine', label: 'Combine', color: '#6366f1' },
    ],
  },
];

export default function NodePalette() {
  return (
    <div className="bg-slate-800 rounded-lg border border-slate-700 p-4">
      <h3 className="text-sm font-semibold text-slate-300 mb-4">Node Palette</h3>
      {nodeCategories.map(cat => (
        <div key={cat.label} className="mb-4">
          <p className="text-xs text-slate-500 uppercase tracking-wider mb-2">{cat.label}</p>
          <div className="space-y-1">
            {cat.items.map(item => (
              <div
                key={item.type}
                draggable
                onDragStart={(e) => handleDragStart(e, item.type)}
                className="flex items-center gap-2 px-3 py-2 rounded bg-slate-700/50 hover:bg-slate-700 cursor-grab active:cursor-grabbing text-sm text-slate-300"
              >
                <span className="w-3 h-3 rounded-full flex-shrink-0" style={{ backgroundColor: item.color }} />
                {item.label}
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
