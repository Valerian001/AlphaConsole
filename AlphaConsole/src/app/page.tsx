import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { OrchestrationCanvas } from '@/components/canvas/OrchestrationCanvas';
import { UtilityPanel } from '@/components/panels/UtilityPanel';

export default function Home() {
  return (
    <DashboardLayout>
      <div className="flex-1 flex overflow-hidden">
        {/* The Core Orchestration Workspace */}
        <OrchestrationCanvas />
        
        {/* The Knowledge & Telemetry Panel */}
        <UtilityPanel />
      </div>
    </DashboardLayout>
  );
}
