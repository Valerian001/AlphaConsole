'use client';

import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { useConsole } from '@/context/ConsoleContext';

export default function MemoryPage() {
  const { demoMode } = useConsole();

  return (
    <DashboardLayout>
      <div className="flex-1 p-8 overflow-y-auto">
        <h2 className="text-2xl font-bold mb-6 text-[var(--cyber-blue)]">Semantic Memory Index</h2>
        
        {demoMode ? (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <MemoryStats label="Vector Embeddings" value="12,402" icon="🧠" />
              <MemoryStats label="Project Contexts" value="45" icon="📁" />
            </div>
            
            <div className="mt-8">
              <h3 className="text-sm font-bold text-[#666] uppercase tracking-widest mb-4">Recent Ingestions</h3>
              <div className="space-y-2 font-mono text-xs">
                <div className="p-3 bg-white/5 border border-white/5 rounded-lg text-[#999]">
                  <span className="text-[var(--cyber-blue)]">[VECTOR]</span> Indexed technical_spec_v2.pdf (1536 dimensions)
                </div>
                <div className="p-3 bg-white/5 border border-white/5 rounded-lg text-[#999]">
                  <span className="text-[var(--cyber-blue)]">[VECTOR]</span> Synced 12 files from github.com/user/alpha-app
                </div>
              </div>
            </div>
          </>
        ) : (
          <div className="mt-20 flex flex-col items-center justify-center text-[var(--text-secondary)] font-mono">
            <div className="text-4xl mb-4 opacity-20">📭</div>
            <div className="text-sm font-bold uppercase tracking-widest">No Live Memory Detected</div>
            <div className="text-[10px] mt-2 opacity-50 text-center max-w-[300px]">
              Memory sync requires an active connection to the Vector Orchestrator. Switch to Demo Mode to see simulated data.
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

const MemoryStats = ({ label, value, icon }: any) => (
  <div className="p-6 rounded-2xl glass border-white/5">
    <div className="text-3xl mb-4">{icon}</div>
    <div className="text-2xl font-bold text-white mb-1">{value}</div>
    <div className="text-xs text-[#666] uppercase tracking-widest">{label}</div>
  </div>
);
