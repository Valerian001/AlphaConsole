# ADR-2026-04-30-DemoMode: Demo Mode for Alpha Console

## Status
Approved

## Context
The Alpha Console currently uses hardcoded dummy data for demonstration purposes. As we move towards full integration with the Go Runtime and NATS control plane, we need a way to switch between this "Demo Mode" (simulated data) and "Live Mode" (real-time data from the backend).

## Decision
1.  **Global State Management**: We will implement a `ConsoleProvider` using React Context to manage a global `demoMode` state.
2.  **Persistence**: The `demoMode` state will be persisted in `localStorage` to maintain the user's preference across sessions.
3.  **UI Control**: A toggle switch will be added to the `UtilityPanel` (or `DashboardLayout`) to allow users to switch modes.
4.  **Data Source Strategy**: 
    *   Components will check the `demoMode` flag.
    *   If `demoMode` is `true`, they will use static mock data.
    *   If `demoMode` is `false`, they will initiate API calls to the backend services.
5.  **Visual Indicators**: When in Demo Mode, a subtle indicator (e.g., a glowing badge or a banner) should be visible to the user.

## Consequences
*   **Pros**: Allows developers and stakeholders to see the console's full potential even when backend services are offline or in development.
*   **Cons**: Increases complexity in components as they must handle two data paths. Potential for confusion if "Live" data is empty or broken.
