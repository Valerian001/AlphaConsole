'use client';

import React, { useState } from 'react';
import { useConsole } from '@/context/ConsoleContext';

export const UtilityPanel = () => {
  const [activeTab, setActiveTab] = useState('LOGS');
  const { demoMode, toggleDemoMode } = useConsole();

  return (
    <div className="hidden md:flex w-[400px] h-full bg-[var(--surface-elevated)] border-l border-[var(--border-muted)] flex-col z-10 shadow-2xl">
      {/* Tabs */}
      <div className="flex p-1 bg-black/20 border-b border-[var(--border-muted)]">
        <Tab label="Live Logs" active={activeTab === 'LOGS'} onClick={() => setActiveTab('LOGS')} />
        <Tab label="Project Assets" active={activeTab === 'ASSETS'} onClick={() => setActiveTab('ASSETS')} />
      </div>

      <div className="flex-1 overflow-y-auto p-5 font-mono">
        {activeTab === 'LOGS' ? (
          <div className="space-y-3">
            <LogEntry time="15:42:01" type="INFO" msg="Starting Developer Agent..." />
            <LogEntry time="15:42:05" type="THOUGHT" msg="Analyzing repository structure in /src/app..." />
            <LogEntry time="15:42:40" type="INFO" msg="Identified missing component: 'AuthGuard'" />
            <LogEntry time="15:42:45" type="INFO" msg="Generating implementation plan..." />
            <LogEntry time="15:43:10" type="WARN" msg="High context window usage: 82k tokens" />
            <LogEntry time="15:44:00" type="ACTION" msg="Writing file: src/app/auth/guard.ts..." />
          </div>
        ) : (
          <div className="space-y-3">
            <AssetItem name="Architecture_Specs.pdf" type="DOC-01" size="1.2 MB" />
            <AssetItem name="Dashboard_Mockup.png" type="IMG-01" size="4.5 MB" />
            <AssetItem name="NATS_Schema.json" type="CODE-01" size="12 KB" />
          </div>
        )}
      </div>

      {/* Demo Mode Toggle */}
      <div className="p-4 border-t border-[var(--border-muted)] bg-black/10">
        <div className="flex items-center justify-between">
          <div className="flex flex-col">
            <span className="text-[10px] font-bold text-white tracking-widest uppercase mb-1">Demo Mode</span>
            <span className="text-[9px] text-[var(--text-secondary)]">Using simulated telemetry</span>
          </div>
          <button 
            onClick={toggleDemoMode}
            className={`
              w-12 h-6 rounded-full transition-all duration-500 relative border
              ${demoMode ? 'bg-[var(--cyber-blue)]/20 border-[var(--cyber-blue)]/50' : 'bg-white/5 border-white/10'}
            `}
          >
            <div className={`
              absolute top-1 w-4 h-4 rounded-full transition-all duration-500
              ${demoMode ? 'left-7 bg-[var(--cyber-blue)] shadow-[0_0_10px_var(--cyber-blue-glow)]' : 'left-1 bg-[var(--text-secondary)]'}
            `} />
          </button>
        </div>
      </div>
    </div>
  );
};

const Tab = ({ label, active, onClick }: any) => (
  <button 
    onClick={onClick}
    className={`flex-1 py-3 text-[11px] font-bold uppercase tracking-widest rounded-lg transition-all
      ${active ? 'bg-white/5 text-white' : 'text-[var(--text-secondary)] hover:text-white'}
    `}
  >
    {label}
  </button>
);

const LogEntry = ({ time, type, msg }: any) => {
  const typeColors: any = {
    INFO: 'text-[var(--cyber-blue)]',
    THOUGHT: 'text-[#777] italic',
    WARN: 'text-[var(--warning)]',
    ACTION: 'text-white font-bold',
    ERROR: 'bg-[var(--danger)] text-white px-1'
  };

  return (
    <div className="text-[12px] leading-relaxed flex gap-2">
      <span className="text-[var(--text-secondary)] opacity-50">[{time}]</span>
      <span className={`font-bold ${typeColors[type] || 'text-white'}`}>[{type}]</span>
      <span className="text-[#d1d1d1]">{msg}</span>
    </div>
  );
};

const AssetItem = ({ name, type, size }: any) => (
  <div className="flex items-center justify-between p-4 rounded-xl bg-white/5 border border-transparent hover:border-[var(--cyber-blue)]/30 transition-all cursor-pointer group">
    <div className="flex items-center gap-4">
      <div className="w-9 h-9 rounded-lg bg-white/5 flex items-center justify-center text-[10px] font-bold text-[var(--text-secondary)] group-hover:text-[var(--cyber-blue)] group-hover:bg-[var(--cyber-blue)]/5 transition-all">
        {type.split('-')[0]}
      </div>
      <div>
        <div className="text-white text-sm font-medium">{name}</div>
        <div className="text-[10px] text-[var(--text-secondary)] mt-1">{type} • {size}</div>
      </div>
    </div>
    <div className="w-1.5 h-1.5 rounded-full bg-[var(--success)] shadow-[0_0_8px_var(--success)]" />
  </div>
);
