'use client';

import { DashboardLayout } from '@/components/layout/DashboardLayout';

export default function SettingsPage() {
  return (
    <DashboardLayout>
      <div className="flex-1 p-8 overflow-y-auto">
        <h2 className="text-2xl font-bold mb-6 text-[var(--cyber-blue)]">Platform Settings</h2>
        <div className="max-w-2xl space-y-8">
          <section>
            <h3 className="text-sm font-bold text-[#666] uppercase tracking-widest mb-4">Worker Configuration</h3>
            <div className="p-6 rounded-2xl glass border-white/5 space-y-4">
              <SettingItem label="Warm Pool Size" value="5 Agent Shells" />
              <SettingItem label="Default GPU" value="NVIDIA RTX 4090" />
              <SettingItem label="Inference Model" value="Qwen 3.6 (27B)" />
            </div>
          </section>

          <section>
            <h3 className="text-sm font-bold text-[#666] uppercase tracking-widest mb-4">Infrastructure Sync</h3>
            <div className="p-6 rounded-2xl glass border-white/5 space-y-4">
              <SettingItem label="NATS JetStream" value="CONNECTED" success />
              <SettingItem label="Supabase DB" value="CONNECTED" success />
              <SettingItem label="Contabo S3" value="CONNECTED" success />
            </div>
          </section>
        </div>
      </div>
    </DashboardLayout>
  );
}

const SettingItem = ({ label, value, success = false }: any) => (
  <div className="flex items-center justify-between py-2">
    <span className="text-sm text-[#999]">{label}</span>
    <span className={`text-sm font-mono ${success ? 'text-[var(--success)]' : 'text-white'}`}>{value}</span>
  </div>
);
