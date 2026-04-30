# Developer Agent Initialization Specification

This document defines the technical "Hydration" process and runtime context for the **Developer Agent**, the execution core responsible for code generation, testing, and debugging within a secure sidecar sandbox.

---

## 1. Initialization Manifest (JSON Payload)

When the Go Runtime hydrates a shell into a Developer, it injects the following `runtime_manifest.json`:

```json
{
  "agent_id": "dev-zeta-04",
  "role": "DEVELOPER",
  "task_context": {
    "project_id": "proj_98231",
    "parent_task_id": "task_1102",
    "subtask_objective": "Implement JWT middleware and login route",
    "target_branch": "feature/auth-core",
    "workspace_root": "/workspace/proj_98231"
  },
  "runtime_environment": {
    "language": "TypeScript",
    "framework": "Next.js",
    "package_manager": "Yarn v4",
    "lsp_enabled": true
  },
  "capabilities": [
    "TERMINAL_ACCESS",
    "FILE_EDIT",
    "GIT_COMMIT",
    "RUN_TESTS",
    "DEBUG_PROCESS"
  ],
  "sandbox_config": {
    "docker_image": "agentops/dev-runtime-node:20-alpine",
    "memory_limit": "8GB",
    "cpu_shares": 1024,
    "network_egress": "RESTRICTED"
  }
}
```

---

## 2. Toolset Configuration (Injection)

The Developer is initialized with a "Full-Stack Engineer" toolset bridge:

| Tool Name | Scope | Description |
| :--- | :--- | :--- |
| `execute_command` | `TERMINAL` | Runs shell commands (npm, git, ls, etc.) inside the sidecar sandbox. |
| `modify_file` | `WORKSPACE` | Precise line-based editing and full-file replacement of source code. |
| `git_manage` | `REPO` | Handles branching, staging, and committing to the project repository. |
| `lsp_query` | `LANGUAGE_SERVER` | Queries the local Language Server for diagnostics, completions, and definition lookups. |
| `submit_result` | `INTERNAL` | Tool to report task completion and provide a summary of changes to the Reviewer. |

---

## 3. Initialization Logic (Sequence)

1.  **Sandbox Provisioning:**
    *   Go Runtime pulls the specific `docker_image` defined in the manifest.
    *   Creates a dedicated Docker network and volume for the task.
2.  **Sidecar Activation:**
    *   Spawns the **Developer Sidecar Container**.
    *   Mounts the project codebase and the `runtime_manifest.json`.
3.  **Language Server Bootstrap:**
    *   Initializes the LSP (e.g., `tsserver`) in the background to provide real-time code intelligence to the agent.
4.  **Task Hydration:**
    *   Agent Shell reads the `subtask_objective`.
    *   Performs a "Quick Scan" of the relevant files to build local context.
5.  **Status Pulse:** Publishes `agent.dev.ready` to NATS and begins the coding cycle.

---

## 4. Resource Allocation (Sandbox)

*   **Runtime:** Docker Sidecar (AgentOps Dev Runtime).
*   **Memory Limit:** 8GB RAM (System + LSP overhead).
*   **Storage:** 10GB ephemeral workspace volume.
*   **Networking:** Restricted. Access to internal Control Plane and approved package registries (npm/pypi) only.
