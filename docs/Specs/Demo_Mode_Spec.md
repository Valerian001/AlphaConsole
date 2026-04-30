# Demo Mode Specification

## Overview
The "Demo Mode" allows the Alpha Console to operate in a simulated environment using pre-defined mock data. This is essential for testing UI/UX and demonstrating capabilities without requiring a live backend.

## Functional Requirements
1.  **Toggle Mechanism**: A user-accessible switch to enable/disable Demo Mode.
2.  **Default State**: Demo Mode should be `ON` by default for new users.
3.  **State Persistence**: The mode must persist across page refreshes.
4.  **Component Behavior**:
    *   **Orchestration Canvas**: In Demo Mode, show a simulated flow of agents (Planner -> Reviewer -> Developer). In Live Mode, show actual agent activity fetched from the NATS stream.
    *   **Memory Index**: In Demo Mode, show mock vector embeddings and ingestion history. In Live Mode, query the actual vector database.
    *   **Telemetry**: In Demo Mode, show simulated GPU/CPU usage. In Live Mode, show real metrics from the Vast.ai instance.

## Non-Functional Requirements
1.  **Low Latency**: Switching modes should be instantaneous (UI update).
2.  **Feedback**: Provide clear visual feedback when Demo Mode is active.

## Technical Details
*   **Context API**: `ConsoleContext`
*   **Storage**: `localStorage.getItem('alpha_demo_mode')`
*   **Hook**: `useConsole()` to access `demoMode` and `toggleDemoMode`.
