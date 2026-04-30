# Design System: Component Library

This document defines the core UI components for the AgentOps platform, following the **Obsidian Flow** aesthetic.

---

## 1. Buttons

Buttons should feel tactile and high-tech, using subtle glows and transitions.

| Type | Visual Style | State (Hover/Active) |
| :--- | :--- | :--- |
| **Primary** | Background: `#00A3FF`, Text: White | Increase brightness + Blue shadow glow. |
| **Secondary** | Glass background, Border: `Border-Sharp` | Background becomes slightly more opaque. |
| **Ghost** | Transparent, Border: None, Text: `Cyber-Blue` | Background: `rgba(0, 163, 255, 0.1)`. |
| **Danger** | Background: `#FF3B3B`, Text: White | Red shadow glow + Scale down (0.98). |

---

## 2. Cards & Panels (The "Glass" Container)

The foundation of the dashboard layout.

*   **Background:** `rgba(18, 18, 18, 0.7)`
*   **Backdrop Blur:** `12px`
*   **Border:** `1px solid rgba(255, 255, 255, 0.05)`
*   **Corner Radius:** `12px` (Modern, rounded but sharp)
*   **Padding:** `20px` (Standard) or `12px` (Compact).

---

### 3. Modals & Overlays
*   **Standard Modal:** Background blur (15px), elevated surface (#121212), and cyber-blue primary actions.
*   **Asset Preview Modal:** Fixed-position overlay (80% viewport) with a dark glassmorphism aesthetic for viewing project documents and wireframes.
*   **Intake Center:** Specialized full-screen modal for project-level data entry.

### 4. Specialized Dash Panels
*   **Utility Panel:** A tabbed vertical container for high-density information (Logs/Assets) that minimizes horizontal footprint.
 the background content.
*   **Container:** Large Glass Card centered on the screen.
*   **Animation:** Scale-up + Fade-in from center.
*   **Close Action:** Top-right "X" or clicking outside the container.

---

## 4. Input Fields & Selects

*   **Background:** `#121212` (Solid, non-glass for contrast).
*   **Border:** `1px solid #262626`.
*   **Focus State:** Border becomes `#00A3FF` with a 2px outer glow.
*   **Typography:** Body (14px Inter).
*   **Placeholder:** Muted gray text.

---

## 5. Agent Status Cards (Specialized)

Specific cards used in the sidebar to track worker health.

*   **Header:** Agent Icon + Name + Status Indicator (Pulse).
*   **Stats Section:** Compact grid showing CPU/Memory usage and Current Stage.
*   **Mini-Log:** The last 3 lines of the agent's log stream in JetBrains Mono.
*   **Action Row:** Buttons for "Pause", "View Full Logs", or "Terminate".

---

## 6. Micro-Animations

*   **Transitions:** Use `cubic-bezier(0.4, 0, 0.2, 1)` for all transforms.
*   **Glows:** Pulsing glows for "Running" states should be soft and slow (2s duration).
*   **Loading:** A thin "scanning" line that moves across glass panels when data is being fetched.
