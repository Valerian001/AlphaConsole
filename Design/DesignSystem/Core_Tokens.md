# Design System: Core Tokens

**Theme Name:** Obsidian Flow (Cyber-Professional Dark)  
**Philosophy:** Precision, Clarity, and High-Performance.

---

## 1. Color Palette

### 1.1 Neutral / Backgrounds
*   **Surface-Deep:** `#080808` (Main backdrop)
*   **Surface-Elevated:** `#121212` (Cards and panels)
*   **Surface-Highlight:** `#1A1A1A` (Hover states)
*   **Border-Muted:** `#262626`
*   **Border-Sharp:** `#3A3A3A`

### 1.2 Brand / Primary
*   **Cyber-Blue:** `#00A3FF` (Main action color)
*   **Blue-Glow:** `rgba(0, 163, 255, 0.15)`
*   **Accent-Gold:** `#FFD700` (Premium status/highlights)

### 1.3 Semantic
*   **Success:** `#00E599` (Agent task complete)
*   **Warning:** `#FFAA00` (Agent retry/pause)
*   **Danger:** `#FF3B3B` (System failure/error)
*   **Info:** `#00A3FF`

---

## 2. Typography

*   **Primary Font:** `Inter` (Sans-serif) - Used for all UI elements, labels, and navigation.
*   **Monospace Font:** `JetBrains Mono` - Used for agent logs, terminal outputs, and code artifacts.

### Type Scale
| Level | Size | Weight | Line-Height |
| :--- | :--- | :--- | :--- |
| **H1** | 32px | 700 | 1.2 |
| **H2** | 24px | 600 | 1.3 |
| **H3** | 18px | 600 | 1.4 |
| **Body** | 14px | 400 | 1.5 |
| **Small** | 12px | 500 | 1.5 |
| **Monospaced**| 13px | 400 | 1.6 |

---

## 3. Glassmorphism & Elevation

*   **Standard Glass:**
    *   `background: rgba(18, 18, 18, 0.7)`
    *   `backdrop-filter: blur(12px)`
    *   `border: 1px solid rgba(255, 255, 255, 0.05)`
*   **Elevated Shadow:** `0 8px 32px 0 rgba(0, 0, 0, 0.8)`

---

## 4. Agent Status Visuals

| Status | Color | Animation |
| :--- | :--- | :--- |
| **Running** | `Cyber-Blue` | Subtle pulse (1.5s) |
| **Paused (HITL)**| `Warning` | Static Glow |
| **Complete** | `Success` | Sharp fade-in |
| **Failed** | `Danger` | Shake + Glow |
