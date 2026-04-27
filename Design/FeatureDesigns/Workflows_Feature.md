# Feature Design: Workflows Module

The Workflows module allows users to define the sequence, branching logic, and agent assignment for repetitive autonomous tasks.

---

## 1. Core Logic
*   **Blueprint System:** Workflows are stored as "Blueprints" in PostgreSQL.
*   **DAG Visualization:** Uses a directed acyclic graph (DAG) to represent stages.
*   **Stage Types:** 
    *   `Linear`: Sequential execution.
    *   `Parallel`: Multiple agents working simultaneously (fan-out).
    *   `Approval`: HITL gates that pause execution.

---

## 2. Visual Requirements
*   **Canvas Editor:** A drag-and-drop interface for connecting agent nodes.
*   **Template Library:** Pre-defined workflows for common tasks (e.g., "Full Stack Feature", "Bug Fix & Test").
*   **Stage Config:** A side-panel for configuring model quantization and context windows per stage.

---

## 3. Interaction Patterns
*   **Simulation Mode:** Preview the message flow through the NATS subjects before live execution.
*   **Versioning:** Ability to clone and iterate on workflow blueprints.
