import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Workflow, Play, Bot, Wrench, BarChart3, History, Settings, ChevronLeft, ChevronRight } from 'lucide-react';

const navItems = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/workflows', icon: Workflow, label: 'Workflows' },
  { to: '/executions', icon: Play, label: 'Executions' },
  { to: '/agents', icon: Bot, label: 'Agents' },
  { to: '/tools', icon: Wrench, label: 'Tools' },
  { to: '/monitoring', icon: BarChart3, label: 'Monitoring' },
  { to: '/history', icon: History, label: 'History' },
  { to: '/settings', icon: Settings, label: 'Settings' },
];

export default function Sidebar({ isOpen, onToggle }) {
  return (
    <aside className={`bg-slate-800 border-r border-slate-700 flex flex-col transition-all duration-200 ${isOpen ? 'w-56' : 'w-16'}`}>
      <div className="h-16 flex items-center justify-center border-b border-slate-700">
        {isOpen ? (
          <span className="font-bold text-sm">LANGGRAPH</span>
        ) : (
          <span className="font-bold text-xs">LG</span>
        )}
      </div>
      <nav className="flex-1 py-4">
        {navItems.map(item => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === '/'}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 text-sm transition-colors ${
                isActive ? 'bg-slate-700 text-white border-r-2 border-blue-500' : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
              }`
            }
          >
            <item.icon size={18} />
            {isOpen && <span>{item.label}</span>}
          </NavLink>
        ))}
      </nav>
      <button onClick={onToggle} className="h-12 flex items-center justify-center border-t border-slate-700 text-slate-400 hover:text-white">
        {isOpen ? <ChevronLeft size={18} /> : <ChevronRight size={18} />}
      </button>
    </aside>
  );
}
