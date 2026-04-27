# Feature Design: Workflows Module

The Workflows module allows users to define the sequence, branching logic, and agent assignment for repetitive autonomous tasks.

---

## 1. Core Logic
*   **Blueprint System:** Workflows are stored as "Blueprints" in PostgreSQL.
*   **DAG Visualization:** Uses a directed acyclic graph (DAG) to represent stages.
*   **Stage Types:** 
    *   `Linear`: Sequential execution.
    *   `Parallel`: Multiple agents working simultaneously (fan-out).
    *   **`Agile-Loop`**: Recursive refinement between Planner and Reviewer agents.
    *   `Approval`: HITL gates that pause execution for User feedback.

---

## 2. The Agile Orchestration Flow

1.  **Stage 1: Planning Loop (Internal)**
    *   Planner creates a draft.
    *   Reviewer critiques and recycles if necessary.
2.  **Stage 2: Human Oversight (Console)**
    *   Reviewer presents the technical draft to the User.
    *   **Contextual Referencing:** The User can use indexing IDs (e.g., "See DOC-01") to point the Planner toward specific attached project documents.
    *   User provides comments or approval.
3.  **Stage 3: Multi-Agent Dispatch (Reviewer-Led)**
    *   Reviewer identifies specialized agents (Developer, Tester).
    *   Reviewer monitors parallel execution of sub-tasks.
*   **Canvas Editor:** A drag-and-drop interface for connecting agent nodes.
*   **Template Library:** Pre-defined workflows for common tasks (e.g., "Full Stack Feature", "Bug Fix & Test").
*   **Stage Config:** A side-panel for configuring model quantization and context windows per stage.

---

## 3. Interaction Patterns
*   **Simulation Mode:** Preview the message flow through the NATS subjects before live execution.
*   **Versioning:** Ability to clone and iterate on workflow blueprints.
