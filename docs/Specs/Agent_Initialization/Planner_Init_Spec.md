# Planner Agent Initialization Specification

This document defines the technical "Hydration" process and runtime context for the **Planner Agent** within the AlphaConsole architecture.

---

## 1. Initialization Manifest (JSON Payload)

When the Go Runtime hydrates a shell into a Planner, it injects the following `runtime_manifest.json`:

```json
{
  "agent_id": "planner-alpha-01",
  "role": "PLANNER",
  "project_context": {
    "project_id": "proj_98231",
    "intake_bucket": "project-intake/proj_98231",
    "qdrant_collection": "memory_proj_98231",
    "github_repo": "https://github.com/user/repo",
    "mode": "NEW_PROJECT" | "LEGACY_TRANSFORMATION"
  },
  "capabilities": [
    "READ_FILES",
    "QUERY_VECTOR_DB",
    "CLONE_REPO",
    "PARSE_CODE",
    "GENERATE_TASK_DAG"
  ],
  "constraints": {
    "max_subtasks_per_iteration": 8,
    "require_reviewer_approval": true,
    "allow_code_execution": false
  }
}
```

---

## 2. Toolset Configuration (Injection)

The Planner is initialized with a specialized toolset bridge:

| Tool Name | Scope | Description |
| :--- | :--- | :--- |
| `analyze_intake` | `project-intake/*` | Scans PDFs and text files for high-level requirements. |
| `visual_analysis` | `project-intake/*.{png,jpg}` | Triggers a Vision LLM (Qwen-VL) to extract UI/UX constraints from wireframes. |
| `query_memory` | `qdrant/project_id` | Performs semantic search across previously indexed project documentation. |
| `git_inspect` | `READ_ONLY` | Clones the repository using the user's PAT to understand current architecture. |
| `propose_objective` | `INTERNAL` | Tool to emit the decided **Objective Name** and **Implementation Plan**. |

---

## 3. Initialization Logic (Sequence)

1.  **Shell Activation:** Go Runtime selects an idle Python shell from the Warm Pool.
2.  **Environment Setup:** 
    *   Injects the `GITHUB_PAT` (encrypted) from the Control Plane.
    *   Sets `OLLAMA_HOST` to the local worker inference endpoint.
3.  **Bootstrapping Thought Process:**
    *   **Phase A: Ingestion.** Planner calls `analyze_intake` to build its internal mental model of the project.
    *   **Phase B: Alignment.** Planner queries `git_inspect` to compare requirements against existing code (if legacy).
    *   **Phase C: Synthesis.** Planner generates the initial Implementation Plan (ADR format).
4.  **Handoff:** Planner publishes its output to `agent.planner.output` and transitions to `AWAITING_REVIEW`.

---

## 4. Resource Allocation (Sandbox)

*   **Runtime:** Python 3.12 (Isolated Process).
*   **Memory Limit:** 4GB RAM (System).
*   **GPU Limit:** Dedicated access to the RTX 4090 inference stream (shared with Ollama).
*   **Networking:** Restricted. Only allowed to communicate with Local Ollama, Local Qdrant, and the GitHub API.
