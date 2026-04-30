# Demo Mode Toggle Design

## UI Components

### 1. The Toggle Switch
*   **Location**: Bottom of the `UtilityPanel` or top-right of the `DashboardLayout` header.
*   **Style**: Cyber-themed toggle. 
    *   **Background**: Deep slate with a subtle inner shadow.
    *   **Thumb**: Glowing cyan (when ON), muted gray (when OFF).
    *   **Label**: "DEMO MODE" in a mono font, uppercase.
*   **Micro-animation**: Smooth transition of the thumb and a pulse effect when activated.

### 2. Status Indicator
*   **Location**: Beside the logo or in the status bar.
*   **Visual**: A small badge `[DEMO]` with a slow breathing glow in `var(--cyber-blue)`.

## UX Flow
1.  User clicks the toggle.
2.  A brief loading animation (simulated) plays to give a "syncing" feel.
3.  The UI updates immediately with the corresponding data set.
4.  A toast notification or status message confirms the mode change.

## Color Palette
*   **Active**: `var(--cyber-blue)` (#00f2ff)
*   **Inactive**: `var(--text-secondary)` (#666)
*   **Glow**: `rgba(0, 242, 255, 0.3)`
