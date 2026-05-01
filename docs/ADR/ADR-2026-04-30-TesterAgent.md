# ADR-2026-04-30-TesterAgent: Implementation of the Tester Agent Shell

## Status
Approved

## Context
The "Gap Analysis" and automated system audit identified that the `Tester Agent` shell (`tester_agent.py`) is missing from the `agents/` directory. This agent is critical for the "Agile-Loop" verification phase, responsible for unit testing, integration testing, and UI verification.

## Decision
1.  **Inheritance**: The `TesterAgent` will inherit from `BaseAgentShell` in `agents/core/base_shell.py` to ensure consistent logging and manifest handling.
2.  **Hydration**: It will consume the `runtime_manifest.json` as defined in `Tester_Init_Spec.md`, specifically the `verification_context` and `qa_requirements`.
3.  **Tooling**: Implement method stubs for the specialized QA toolset:
    *   `execute_test_suite()`
    *   `simulate_user_flow()`
    *   `audit_app_logs()`
    *   `scan_vulnerabilities()`
    *   `emit_test_report()`
4.  **Workflow Phase**: The `run()` loop will follow the sequence defined in the spec: Sandbox Provisioning -> Env Preparation -> Verification Phases (Unit/Integration/UX) -> Reporting.

## Consequences
*   **Pros**: Completes the core agent pool. Enables automated verification in the orchestration loop.
*   **Cons**: Initial tool implementations will be stubs that rely on the sandbox environment being correctly provisioned by the Go Runtime.
