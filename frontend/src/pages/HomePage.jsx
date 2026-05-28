import React from 'react';
import { useWorkflows } from '../hooks/useWorkflow';
import { useMonitoring } from '../hooks/useMonitoring';
import { Workflow, Play, BarChart3, Activity } from 'lucide-react';

export default function HomePage() {
  const { workflows } = useWorkflows();
  const { summary } = useMonitoring();

  const stats = [
    { label: 'Workflows', value: workflows.length, icon: Workflow, color: 'text-blue-400 bg-blue-900/30 border-blue-800' },
    { label: 'Executions', value: summary?.total_executions || 0, icon: Play, color: 'text-green-400 bg-green-900/30 border-green-800' },
    { label: 'Errors', value: summary?.total_errors || 0, icon: Activity, color: 'text-red-400 bg-red-900/30 border-red-800' },
    { label: 'Active', value: workflows.filter(w => w.status === 'active').length, icon: BarChart3, color: 'text-purple-400 bg-purple-900/30 border-purple-800' },
  ];

  return (
    <div>
      <h2 className="text-2xl font-bold text-white mb-6">Dashboard</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {stats.map(stat => (
          <div key={stat.label} className={`rounded-lg border p-4 ${stat.color}`}>
            <div className="flex items-center justify-between">
              <span className="text-sm">{stat.label}</span>
              <stat.icon size={20} />
            </div>
            <p className="text-3xl font-bold mt-2">{stat.value}</p>
          </div>
        ))}
      </div>
      <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
        <h3 className="text-lg font-semibold text-white mb-4">Welcome to LangGraph Workflow Engine</h3>
        <p className="text-slate-400 text-sm leading-relaxed">
          Build, execute, and monitor AI agent workflows using a visual drag-and-drop interface.
          Create custom workflows with LLM-powered agents, decision trees, data pipelines, and more.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
          {[
            { title: 'Visual Builder', desc: 'Drag-and-drop workflow canvas' },
            { title: 'Multi-Agent', desc: 'Orchestrate multiple AI agents' },
            { title: 'Monitoring', desc: 'Real-time execution tracking' },
          ].map(item => (
            <div key={item.title} className="bg-slate-700/30 rounded p-3 border border-slate-600">
              <p className="text-sm font-medium text-white">{item.title}</p>
              <p className="text-xs text-slate-400 mt-1">{item.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
