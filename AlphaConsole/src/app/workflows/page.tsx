'use client';

import { DashboardLayout } from '@/components/layout/DashboardLayout';

export default function WorkflowsPage() {
  return (
    <DashboardLayout>
      <div className="flex-1 p-8 overflow-y-auto">
        <h2 className="text-2xl font-bold mb-6 text-[var(--cyber-blue)]">Workflow Orchestrator</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <WorkflowCard name="Standard Fleet Pipeline" tasks={12} active />
          <WorkflowCard name="Legacy Transformation" tasks={8} />
          <WorkflowCard name="Security Audit Loop" tasks={4} />
        </div>
      </div>
    </DashboardLayout>
  );
}

const WorkflowCard = ({ name, tasks, active = false }: any) => (
  <div className={`p-6 rounded-2xl glass transition-all cursor-pointer group ${active ? 'border-[var(--cyber-blue)]/50' : ''}`}>
    <div className="flex items-center justify-between mb-4">
      <div className="w-10 h-10 rounded-xl bg-[var(--cyber-blue)]/10 flex items-center justify-center text-[var(--cyber-blue)]">
        ⚡
      </div>
      <div className={`text-[10px] font-bold uppercase tracking-widest px-2 py-1 rounded bg-white/5 ${active ? 'text-[var(--success)]' : 'text-[#666]'}`}>
        {active ? 'Active' : 'Idle'}
      </div>
    </div>
    <h3 className="font-bold text-white mb-1 group-hover:text-[var(--cyber-blue)] transition-colors">{name}</h3>
    <p className="text-xs text-[#666]">{tasks} Automated Stages</p>
  </div>
);
