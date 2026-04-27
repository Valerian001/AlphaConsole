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

### 2.1 The Evolution Canvas
*   **Dynamic Layout:** An auto-arranging tree graph that expands as agents decompose tasks.
*   **Interaction:** Clicking a node in the tree focuses the Log Stream on that specific task's output.
*   **Animations:** Uses the "Data Particle" effect on connectors to show active data transfer between agents.

### 2.2 Global Status Bar
*   **Infrastructure Health:** Shows connection status to Supabase, NATS, and the active Vast.ai region (e.g., ZA1).
*   **Performance Metrics:** Real-time TFLOPS and VRAM headroom visualization.

---

## 3. Interaction Patterns

### 3.1 Command Palette (Ctrl+K)
*   Quick navigation between modules.
*   Instant task creation or agent termination.
*   "Emergency Stop" command to kill all active Vast.ai instances.

### 3.2 Human-in-the-Loop Gates
*   Visual cues (Warning Pulse) when an agent is stuck or awaiting approval.
*   One-click "Resume" or "Edit & Continue" from the dashboard canvas.
