'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { IntakeModal } from '../modals/IntakeModal';
import { useConsole } from '@/context/ConsoleContext';

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export const DashboardLayout: React.FC<DashboardLayoutProps> = ({ children }) => {
  const [isIntakeOpen, setIsIntakeOpen] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const { demoMode } = useConsole();
  const pathname = usePathname();

  return (
    <div className="flex h-screen w-full bg-[var(--bg-deep)] text-white relative">
      {/* Sidebar Mobile Backdrop */}
      {isSidebarOpen && (
        <div 
          className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 md:hidden"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside className={`
        fixed inset-y-0 left-0 z-50 w-[280px] bg-[var(--surface-elevated)] border-r border-[var(--border-muted)] p-6 flex flex-col gap-8 transition-transform duration-300
        md:relative md:translate-x-0
        ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
      `}>
        <div className="flex items-center justify-between md:justify-start gap-3">
          <div className="flex items-center gap-3 text-xl font-bold tracking-tight">
            <div className="w-6 h-6 bg-[var(--cyber-blue)] rounded-md shadow-[0_0_10px_var(--cyber-blue-glow)]" />
            ALPHA<span className="text-[var(--cyber-blue)]">CONSOLE</span>
            {demoMode && (
              <span className="text-[10px] bg-[var(--cyber-blue)]/20 text-[var(--cyber-blue)] px-2 py-0.5 rounded border border-[var(--cyber-blue)]/30 animate-pulse ml-2">
                DEMO
              </span>
            )}
          </div>
          <button onClick={() => setIsSidebarOpen(false)} className="md:hidden text-[var(--text-secondary)] hover:text-white">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>
        
        <nav className="flex flex-col gap-2">
          <NavItem href="/" label="Dashboard" active={pathname === '/'} onClick={() => setIsSidebarOpen(false)} />
          <NavItem href="/workflows" label="Workflows" active={pathname === '/workflows'} onClick={() => setIsSidebarOpen(false)} />
          <NavItem href="/agents" label="Agents" active={pathname === '/agents'} onClick={() => setIsSidebarOpen(false)} />
          <NavItem href="/memory" label="Memory" active={pathname === '/memory'} onClick={() => setIsSidebarOpen(false)} />
          <NavItem href="/settings" label="Settings" active={pathname === '/settings'} onClick={() => setIsSidebarOpen(false)} />
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0">
        <header className="h-[72px] border-b border-[var(--border-muted)] flex items-center justify-between px-4 md:px-8">
          <div className="flex items-center gap-4">
            <button 
              onClick={() => setIsSidebarOpen(true)}
              className="p-2 -ml-2 text-[var(--text-secondary)] hover:text-white md:hidden"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" /></svg>
            </button>
            <div className="flex items-center gap-3">
              <span className="text-xs text-[var(--text-secondary)] hidden sm:inline">System Status:</span>
              <span className="text-[10px] sm:text-xs font-bold text-[var(--success)] uppercase tracking-widest flex items-center gap-2">
                <div className="w-1.5 h-1.5 rounded-full bg-[var(--success)] animate-pulse" />
                <span className="hidden xs:inline">AlphaConsole Active (ZA1)</span>
                <span className="xs:hidden">ZA1 ACTIVE</span>
              </span>
            </div>
          </div>
          
          <button 
            onClick={() => setIsIntakeOpen(true)}
            className="bg-[var(--cyber-blue)] hover:brightness-110 text-white px-3 sm:px-5 py-2 sm:py-2.5 rounded-lg text-xs sm:text-sm font-bold transition-all shadow-[0_4px_15px_var(--cyber-blue-glow)]"
          >
            <span className="hidden sm:inline">+ New Objective</span>
            <span className="sm:hidden">+ NEW</span>
          </button>
        </header>

        <div className="flex-1 flex overflow-hidden">
          {children}
        </div>

        <IntakeModal isOpen={isIntakeOpen} onClose={() => setIsIntakeOpen(false)} />
      </main>
    </div>
  );
};

const NavItem = ({ href, label, active = false, onClick }: { href: string; label: string; active?: boolean; onClick?: () => void }) => (
  <Link 
    href={href} 
    onClick={onClick}
    className={`flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all
      ${active ? 'bg-[var(--cyber-blue)]/5 text-[var(--cyber-blue)]' : 'text-[var(--text-secondary)] hover:bg-white/5 hover:text-white'}
    `}
  >
    {label}
  </Link>
);
