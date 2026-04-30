# Tester Agent Initialization Specification

This document defines the technical "Hydration" process and runtime context for the **Tester Agent**, the quality assurance core responsible for verifying implementation integrity and generating coverage reports.

---

## 1. Initialization Manifest (JSON Payload)

When the Go Runtime hydrates a shell into a Tester, it injects the following `runtime_manifest.json`:

```json
{
  "agent_id": "test-delta-09",
  "role": "TESTER",
  "verification_context": {
    "project_id": "proj_98231",
    "parent_task_id": "task_1102",
    "verification_objective": "Verify JWT expiration logic and role-based access",
    "target_branch": "feature/auth-core",
    "test_environment_url": "http://localhost:3000"
  },
  "qa_requirements": {
    "min_coverage_threshold": 80,
    "require_e2e_pass": true,
    "enforce_linting": true
  },
  "capabilities": [
    "EXECUTE_TESTS",
    "BROWSER_AUTOMATION",
    "LOG_AUDIT",
    "LINT_SCAN",
    "REPORT_COVERAGE"
  ],
  "sandbox_config": {
    "docker_image": "agentops/test-runtime-full:latest",
    "memory_limit": "8GB",
    "cpu_shares": 1024,
    "headless_browser": true
  }
}
```

---

## 2. Toolset Configuration (Injection)

The Tester is initialized with a "QA Engineer" toolset bridge:

| Tool Name | Scope | Description |
| :--- | :--- | :--- |
| `execute_test_suite` | `SANDBOX` | Automatically detects and runs Jest, Vitest, Pytest, or Go Test. |
| `simulate_user_flow` | `BROWSER` | Uses Playwright/Puppeteer to verify UI interactions and user journeys. |
| `audit_app_logs` | `RUNTIME` | Monitors the application's stdout/stderr during tests to catch silent errors. |
| `scan_vulnerabilities` | `CODEBASE` | Runs static analysis tools (e.g., Snyk, SonarQube) for security regressions. |
| `emit_test_report` | `INTERNAL` | Tool to report pass/fail status and coverage metrics to the Reviewer. |

---

## 3. Initialization Logic (Sequence)

1.  **Sandbox Provisioning:**
    *   Spawns the **Tester Sidecar**.
    *   Mounts the updated project code (post-Developer commit).
2.  **Environment Preparation:**
    *   Installs test dependencies (if not cached).
    *   Spawns a temporary "Shadow Instance" of the application for integration testing.
3.  **Verification Strategy:**
    *   **Phase 1: Unit.** Verifies logic in isolation.
    *   **Phase 2: Integration.** Verifies the Developer's code against the rest of the system.
    *   **Phase 3: UX (If applicable).** Headless browser verification of critical paths.
4.  **Reporting:**
    *   Tester aggregates all results into a single "Verification Bundle" for the Reviewer.

---

## 4. Resource Allocation (Sandbox)

*   **Runtime:** Docker Sidecar (AgentOps QA Runtime).
*   **Memory Limit:** 8GB RAM.
*   **Networking:** Internal access to the local app shadow and the Control Plane API.
