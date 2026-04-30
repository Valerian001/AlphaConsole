# Design System: Agent Visual Language

This document defines how agents and their states are represented visually across the AgentOps platform.

---

## 1. Agent Archetypes & Icons

Each agent type has a distinct visual identifier to help users quickly differentiate between workflow roles.

| Agent Role | Primary Icon | Accent Color |
| :--- | :--- | :--- |
| **Planner** | `Brain` / `Map` | Cyber-Blue |
| **Developer** | `Code` / `Terminal` | Cyber-Blue |
| **Reviewer** | `Search` / `Shield` | Accent-Gold |
| **Tester** | `Check-Circle` | Success-Green |
| **Marketing** | `Megaphone` | Info-Blue |

---

## 2. Status Indicators (The "Pulse")

Agents use a "Pulse" system to indicate activity without overwhelming the UI with moving parts.

*   **Idle:** Dimmed icon, 50% opacity, no animation.
*   **Active (Processing):** 100% opacity, subtle glowing pulse (2s cycle).
*   **Thinking (Long-running):** Rotating border ring around the agent icon.
*   **HITL / Paused:** Warning-Yellow pulse + "Awaiting Input" badge.

---

## 3. Log Stream Aesthetics

Logs are the primary way users debug agent reasoning. They must be highly readable and scannable.

*   **Font:** JetBrains Mono (13px).
*   **Line Spacing:** 1.6 (Comfortable reading for long reasoning traces).
*   **Color Coding:**
    *   `[INFO]`: Cyber-Blue text.
    *   `[THOUGHT]`: Sophisticated Gray (Italic).
    *   `[ACTION]`: White (Bold).
    *   `[ERROR]`: Danger-Red background + White text.

---

## 4. Node-Graph Visuals (Workflow Builder)

The workflow graph uses a "Flowing Data" aesthetic.

*   **Nodes:** Glassmorphic cards with agent icons.
*   **Edges (Connections):** Neon-Blue lines with animated "Data Particles" moving in the direction of the workflow.
*   **Branching:** Sharp, angled paths for conditional logic; smooth curves for linear pipelines.
