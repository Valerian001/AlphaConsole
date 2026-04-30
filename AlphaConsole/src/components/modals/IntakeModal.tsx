'use client';

import React, { useState } from 'react';

interface IntakeModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const IntakeModal: React.FC<IntakeModalProps> = ({ isOpen, onClose }) => {
  const [description, setDescription] = useState('');
  const [repoUrl, setRepoUrl] = useState('');

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
      <div className="w-full max-w-2xl bg-[var(--surface-elevated)] border border-[var(--border-muted)] rounded-3xl overflow-hidden shadow-2xl flex flex-col">
        {/* Header */}
        <div className="p-8 border-b border-[var(--border-muted)] flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-[var(--cyber-blue)]">NEW OBJECTIVE</h2>
            <p className="text-[10px] text-[var(--text-secondary)] mt-1 uppercase tracking-widest font-bold">Multi-modal Project Intake</p>
          </div>
          <button onClick={onClose} className="text-[var(--text-secondary)] hover:text-white transition-colors text-xl">
            ✕
          </button>
        </div>

        {/* Content */}
        <div className="p-8 space-y-6 overflow-y-auto max-h-[70vh]">
          {/* Text Intake */}
          <div className="space-y-2">
            <label className="text-[11px] font-bold text-[var(--text-secondary)] uppercase tracking-wider">1. Objective Description</label>
            <textarea 
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Describe what you want the fleet to build..."
              className="w-full h-32 bg-black/30 border border-[var(--border-muted)] rounded-2xl p-4 text-sm focus:outline-none focus:border-[var(--cyber-blue)] transition-all placeholder:text-white/10"
            />
          </div>

          {/* Repo Intake */}
          <div className="space-y-2">
            <label className="text-[11px] font-bold text-[var(--text-secondary)] uppercase tracking-wider">2. GitHub Repository (Legacy Context)</label>
            <input 
              type="text"
              value={repoUrl}
              onChange={(e) => setRepoUrl(e.target.value)}
              placeholder="https://github.com/user/repo"
              className="w-full bg-black/30 border border-[var(--border-muted)] rounded-2xl p-4 text-sm focus:outline-none focus:border-[var(--cyber-blue)] transition-all placeholder:text-white/10"
            />
          </div>

          {/* File Upload (Multi-modal) */}
          <div className="space-y-2">
            <label className="text-[11px] font-bold text-[var(--text-secondary)] uppercase tracking-wider">3. Architectural Assets</label>
            <div className="w-full border-2 border-dashed border-[var(--border-muted)] rounded-2xl p-10 flex flex-col items-center justify-center bg-white/5 hover:bg-white/10 hover:border-[var(--cyber-blue)]/30 transition-all cursor-pointer group">
              <div className="w-12 h-12 rounded-xl bg-[var(--cyber-blue)]/10 flex items-center justify-center text-[var(--cyber-blue)] mb-4 group-hover:scale-110 transition-transform">
                ↑
              </div>
              <p className="text-sm font-medium">Drop wireframes, logic flows, or PRDs here</p>
              <p className="text-[10px] text-[var(--text-secondary)] mt-2 uppercase tracking-widest font-bold">Max 50MB per file</p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-8 border-t border-[var(--border-muted)] bg-black/20 flex items-center justify-end gap-4">
          <button onClick={onClose} className="px-6 py-3 text-sm font-bold text-[var(--text-secondary)] hover:text-white transition-colors">
            Cancel
          </button>
          <button className="px-8 py-3 bg-[var(--cyber-blue)] hover:brightness-110 text-white rounded-2xl text-sm font-bold shadow-[0_4px_15px_var(--cyber-blue-glow)] transition-all">
            Initialize Fleet
          </button>
        </div>
      </div>
    </div>
  );
};
