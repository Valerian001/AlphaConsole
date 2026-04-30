# Feature Design: AlphaConsole Dashboard

The Dashboard is the central orchestration hub of AlphaConsole, providing real-time visibility into the autonomous fleet and the evolution of complex objectives.

---

## 1. Core Logic

### 1.1 Task Evolution Engine
*   **Tree Construction:** The dashboard listens to `task.created` and `task.evolved` events via NATS. 
*   **Relationship Mapping:** Automatically maps parent-child relationships between high-level Planner objectives and low-level Developer sub-tasks.
*   **State Propagation:** If a child task fails, the visual "branch" in the evolution tree reflects the error state immediately.

### 1.2 Live Telemetry
*   **Log Streaming:** Aggregates logs from all active agents into a single, filterable WebSocket stream.
*   **Resource Monitoring:** Direct integration with the Vast.ai CLI/API to pull real-time GPU/CPU metrics for the active worker instances.

---

## 2. Visual Requirements

### 2.1 The Infinite Evolution Canvas
*   **Panning & Zooming:** The canvas supports an infinite, coordinate-based workspace, allowing users to move freely across massive agent fleets.
*   **Dynamic Node Spawning:** As the Reviewer dispatches tasks, new agent nodes materialize on the canvas with real-time status pulses.
*   **Agent Work Visualization:** Each active node displays a "Mini-Activity" preview (e.g., "Reading /src/utils.ts" or "Running Jest") to provide instant context without opening logs.
*   **Auto-Layout Engine:** Ensures that complex fanned-out task trees remain readable and organized as the fleet grows.

### 2.2 Global Status Bar
*   **Infrastructure Health:** Shows connection status to Supabase, NATS, and the active Vast.ai region (e.g., ZA1).
*   **Performance Metrics:** Real-time VRAM visualization including:
    *   **Total VRAM:** The hardware limit (e.g., 24GB for RTX 4090).
    *   **Total Currently in Use:** Sum of VRAM consumed by Ollama, agents, and sidecars.
    *   **Total Remaining:** Available headroom for new tasks or context expansion.

---

## 3. Interaction Patterns

### 3.1 Command Palette (Ctrl+K)
*   Quick navigation between modules.
*   Instant task creation or agent termination.
*   "Emergency Stop" command to kill all active Vast.ai instances.

### 3.2 Human-in-the-Loop Gates
*   Visual cues (Warning Pulse) when an agent is stuck or awaiting approval.
*   One-click "Resume" or "Edit & Continue" from the dashboard canvas.

### 3.3 Tabbed Utility Panel (Consolidated Workspace)
*   **Dual-Purpose Hub:** Merges Live Logs and Project Assets into a single right-hand panel to maximize horizontal canvas space.
*   **Asset Preview System:** 
    *   **Modal Overlay:** High-fidelity viewing of project assets (PDF, Images) without navigating away from the dashboard.
    *   **Context Preservation:** Previewing an asset does not interrupt the Live Log stream or agent orchestration.

### 3.3 Project Asset Management
*   **Asset Explorer:** A dedicated panel to view all intake files (PDFs, Images) for the current project.
*   **Lifecycle Control:** 
    *   **Single Delete:** Remove individual files to prune irrelevant context.
    *   **Bulk Actions:** Multi-select and delete multiple assets to reset project context.
    *   **Indexing Sync:** Deleting a file from the dashboard automatically triggers a removal of its semantic chunks from the project's Qdrant collection.
### 3.4 Instance Provisioning Module
*   **On-Demand Spawning:** The dashboard monitors for an active Vast.ai worker. If missing, it triggers the provisioning flow.
*   **Marketplace Filtering:** Automatically filters Vast.ai for RTX 4090s with >500Mbps bandwidth and >16 CPU cores.
*   **Pricing Gate:** Presents a sorted list of matching servers ($/hr). Execution is blocked until the user selects and approves a server cost.
*   **Deployment Tracking:** Visual progress bar showing instance creation, image pulling, and system bootstrap status.
