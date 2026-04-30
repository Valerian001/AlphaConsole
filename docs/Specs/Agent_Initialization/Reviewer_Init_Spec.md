# Reviewer Agent Initialization Specification

This document defines the technical "Hydration" process and runtime context for the **Reviewer Agent**, the primary technical auditor and fleet dispatcher of the AlphaConsole.

---

## 1. Initialization Manifest (JSON Payload)

When the Go Runtime hydrates a shell into a Reviewer, it injects the following `runtime_manifest.json`:

```json
{
  "agent_id": "reviewer-beta-01",
  "role": "REVIEWER",
  "orchestration_context": {
    "project_id": "proj_98231",
    "iteration_count": 3,
    "current_plan_id": "plan_7721",
    "required_specializations": ["frontend", "security"]
  },
  "fleet_matrix": [
    { "type": "DEVELOPER", "specializations": ["React", "Go", "Python"], "instances": 4 },
    { "type": "TESTER", "specializations": ["Cypress", "Pytest"], "instances": 2 }
  ],
  "capabilities": [
    "CRITIQUE_PLAN",
    "QUERY_AGENT_FLEET",
    "VALIDATE_SECURITY",
    "DISPATCH_SUBTASKS",
    "TRIGGER_HUMAN_GATE"
  ],
  "constraints": {
    "max_iterations_before_escalation": 5,
    "enforce_test_coverage": true,
    "require_repo_link": true
  }
}
```

---

## 2. Toolset Configuration (Injection)

The Reviewer is initialized with an "Auditor & Fleet Manager" toolset:

| Tool Name | Scope | Description |
| :--- | :--- | :--- |
| `audit_plan` | `IMPLEMENTATION_PLAN` | Analyzes the Planner's output for security flaws, resource leaks, or missing edge cases. |
| `query_agent_fleet` | `DB:agents_table` | Queries the current pool of active agents to find the best match for subtasks. |
| `validate_intake_match` | `QDRANT / MINIO` | Cross-references the plan against the original indexed project assets (DOC-01, etc.). |
| `recycle_to_planner` | `NATS:agent.planner.input` | Sends feedback back to the Planner for correction. |
| `request_dispatch` | `NATS:task.dispatch` | Triggers the final dispatch to the worker fleet after user approval. |

---

## 3. Initialization Logic (Sequence)

1.  **Shell Activation:** Go Runtime selects an idle Python shell from the Warm Pool.
2.  **Context Synchronization:**
    *   Injects the **current Implementation Plan** as the primary input.
    *   Injects the **Fleet Capability Matrix** so the Reviewer knows who can execute the work.
3.  **Audit Strategy:**
    *   **Phase 1: Technical QA.** Does the plan meet the project requirements from the intake?
    *   **Phase 2: Dispatch Planning.** Which agents should handle which subtasks based on the fleet matrix?
    *   **Phase 3: Security Pass.** Are there any architectural risks (e.g., exposed credentials)?
4.  **Decision Path:**
    *   **If Flawed:** Reviewer calls `recycle_to_planner` with detailed critiques.
    *   **If Approved:** Reviewer calls `request_human_gate` to present the plan to the user.

---

## 4. Resource Allocation (Sandbox)

*   **Runtime:** Python 3.12 (Isolated Process).
*   **Memory Limit:** 6GB RAM (Requires higher memory for complex cross-referencing).
*   **GPU Limit:** Shared inference access for QA reasoning.
*   **Networking:** Restricted. Access to Control Plane API (for fleet queries) and local inference services.
