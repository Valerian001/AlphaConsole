'use client';

import React, { useState, useRef } from 'react';
import { useConsole } from '@/context/ConsoleContext';

export const OrchestrationCanvas = () => {
  const [offset, setOffset] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const { demoMode } = useConsole();
  const containerRef = useRef<HTMLDivElement>(null);

  const handleMouseDown = () => setIsDragging(true);
  const handleMouseUp = () => setIsDragging(false);
  
  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isDragging) return;
    setOffset({
      x: offset.x + e.movementX,
      y: offset.y + e.movementY
    });
  };

  return (
    <div 
      ref={containerRef}
      className="flex-1 relative overflow-hidden bg-[var(--bg-deep)] cursor-grab active:cursor-grabbing"
      onMouseDown={handleMouseDown}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
      onMouseMove={handleMouseMove}
      style={{
        backgroundImage: 'radial-gradient(var(--border-muted) 1px, transparent 1px)',
        backgroundSize: '40px 40px',
        backgroundPosition: `${offset.x}px ${offset.y}px`
      }}
    >
      {demoMode ? (
        <>
          {/* SVG Layer for Animated Paths */}
          <svg className="absolute inset-0 w-full h-full pointer-events-none z-0">
            <defs>
              <linearGradient id="dataGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="var(--cyber-blue)" stopOpacity="0" />
                <stop offset="50%" stopColor="var(--cyber-blue)" stopOpacity="1" />
                <stop offset="100%" stopColor="var(--cyber-blue)" stopOpacity="0" />
              </linearGradient>
            </defs>
            {/* Simplified Path for Demo */}
            <path 
              d="M 200 300 L 400 300" 
              stroke="var(--cyber-blue)" 
              strokeWidth="2" 
              fill="none" 
              className="opacity-20"
            />
            <circle r="3" fill="var(--cyber-blue)">
              <animateMotion 
                path="M 200 300 L 400 300" 
                dur="2s" 
                repeatCount="indefinite" 
              />
            </circle>
          </svg>

          <div 
            className="absolute transition-transform duration-75 flex items-center gap-24 p-24"
            style={{ transform: `translate(${offset.x}px, ${offset.y}px)` }}
          >
            <AgentNode icon="P" label="Planner" status="IDLE" />
            <AgentNode icon="R" label="Reviewer" status="ACTIVE" active />
            <AgentNode icon="H" label="Human Gate" status="WAITING" waiting />
            
            <div className="flex flex-col gap-6 ml-12">
              <AgentNode icon="D" label="Dev-Alpha" status="RUNNING" active activity="> Writing /src/auth.ts" />
              <AgentNode icon="D" label="Dev-Beta" status="RUNNING" active activity="> Parsing DOC-01" />
            </div>
          </div>
        </>
      ) : (
        <div className="absolute inset-0 flex flex-col items-center justify-center text-[var(--text-secondary)] font-mono">
          <div className="w-16 h-16 mb-6 border-2 border-dashed border-[var(--border-muted)] rounded-2xl flex items-center justify-center animate-spin">
             <div className="w-8 h-8 bg-[var(--border-muted)]/20 rounded-lg" />
          </div>
          <div className="text-sm font-bold tracking-[0.2em] uppercase">Connecting to Control Plane...</div>
          <div className="text-[10px] mt-2 opacity-50">Waiting for NATS stream handshake</div>
        </div>
      )}
    </div>
  );
};

const AgentNode = ({ icon, label, status, active, waiting, activity }: any) => (
  <div className={`
    min-w-[160px] p-5 rounded-2xl glass transition-all duration-500
    ${active ? 'border-[var(--cyber-blue)] shadow-[0_0_20px_var(--cyber-blue-glow)]' : 'border-[var(--border-muted)]'}
    ${waiting ? 'border-[var(--warning)] shadow-[0_0_20px_rgba(255,170,0,0.1)]' : ''}
  `}>
    <div className={`
      w-10 h-10 rounded-xl mx-auto mb-3 flex items-center justify-center font-bold text-sm
      ${active ? 'bg-[var(--cyber-blue)]/10 text-[var(--cyber-blue)]' : 'bg-white/5 text-[var(--text-secondary)]'}
      ${waiting ? 'bg-[var(--warning)]/10 text-[var(--warning)]' : ''}
    `}>
      {icon}
    </div>
    <div className="text-sm font-semibold mb-1">{label}</div>
    <div className={`text-[10px] uppercase tracking-widest font-bold ${active ? 'text-[var(--success)]' : 'text-[var(--text-secondary)]'}`}>
      {status}
    </div>
    {activity && (
      <div className="mt-3 pt-3 border-t border-white/5 text-[9px] font-mono text-[var(--cyber-blue)] opacity-80">
        {activity}
      </div>
    )}
  </div>
);
