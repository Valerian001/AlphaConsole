# ADR-2026-04-30-ProductionReadiness: Resolution of Audit Failures and Protocol Alignment

## Status
Accepted

## Context
An automated system audit identified critical failures regarding production readiness and NATS protocol drift. Several components use "In Production" stubs or non-standard messaging subjects that deviate from the `Software_Stack_Specs.md`. These issues must be resolved to ensure system reliability and security.

## Decision
1.  **Security Hardening**:
    *   Restrict FastAPI `allow_origins` to a configurable environment variable (`ALLOWED_ORIGINS`).
2.  **Protocol Alignment**:
    *   Synchronize all NATS subjects to follow the hierarchy in `Software_Stack_Specs.md`.
    *   Objectives and Task creation will use `agent.task.create`.
    *   Agent execution signals will use `agent.worker.{type}.exec`.
    *   Formalize `worker.teardown.complete` in the communication specs.
3.  **Removal of Stubs**:
    *   **Memory Agent**: Implement actual HTTP calls to the Ollama embedding service using `httpx`. Replace dummy vectors with real inference results.
    *   **Tester Agent**: Implement actual command execution for `pytest` and basic `playwright` connectivity checks.
4.  **Worker Runtime**:
    *   Update the Go runtime to subscribe to `agent.worker.*.exec` instead of `task.*.assigned`.

## Consequences
*   **Pros**: Full alignment with technical specifications. Enhanced security posture. Functional RAG and testing pipelines.
*   **Cons**: Requires careful synchronization of subjects across both Go and Python services.
