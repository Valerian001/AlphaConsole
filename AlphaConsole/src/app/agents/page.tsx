'use client';

import { DashboardLayout } from '@/components/layout/DashboardLayout';

export default function AgentsPage() {
  return (
    <DashboardLayout>
      <div className="flex-1 p-8 overflow-y-auto">
        <h2 className="text-2xl font-bold mb-6 text-[var(--cyber-blue)]">Agent Fleet Management</h2>
        <div className="space-y-4">
          <AgentRow role="Planner" status="ACTIVE" load="12%" task="Objective Formulation" />
          <AgentRow role="Reviewer" status="ACTIVE" load="45%" task="Code Quality Audit" />
          <AgentRow role="Developer" status="IDLE" load="0%" task="N/A" />
          <AgentRow role="Tester" status="IDLE" load="0%" task="N/A" />
        </div>
      </div>
    </DashboardLayout>
  );
}

const AgentRow = ({ role, status, load, task }: any) => (
  <div className="flex items-center justify-between p-4 rounded-xl glass border-white/5 hover:border-[var(--cyber-blue)]/30 transition-all">
    <div className="flex items-center gap-4">
      <div className="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center font-bold text-xs text-[var(--cyber-blue)]">
        {role[0]}
      </div>
      <div>
        <div className="font-bold text-sm text-white">{role} Agent</div>
        <div className="text-[10px] text-[#666] uppercase tracking-widest">{task}</div>
      </div>
    </div>
    <div className="flex items-center gap-12 text-right">
      <div>
        <div className="text-[10px] text-[#666] uppercase mb-1">Load</div>
        <div className="text-xs font-mono text-white">{load}</div>
      </div>
      <div className="w-24">
        <div className={`text-[10px] font-bold uppercase tracking-widest ${status === 'ACTIVE' ? 'text-[var(--success)]' : 'text-[#666]'}`}>
          {status}
        </div>
      </div>
    </div>
  </div>
);
