import React from 'react';
import { Menu, Github } from 'lucide-react';

export default function Header({ onMenuClick }) {
  return (
    <header className="h-16 bg-slate-800 border-b border-slate-700 flex items-center justify-between px-6">
      <div className="flex items-center gap-4">
        <button onClick={onMenuClick} className="text-slate-400 hover:text-white p-1">
          <Menu size={20} />
        </button>
        <h1 className="text-lg font-semibold">LangGraph Workflow Engine</h1>
      </div>
      <div className="flex items-center gap-3">
        <span className="text-xs bg-slate-700 text-slate-300 px-2 py-1 rounded">v0.1.0</span>
        <a href="https://github.com" className="text-slate-400 hover:text-white">
          <Github size={18} />
        </a>
      </div>
    </header>
  );
}
