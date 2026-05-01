# ADR-2026-04-30-InfrastructureScaling: Permanent Core Services on Contabo

## Status
Accepted

## Context
The Alpha system relies on a hybrid model where orchestration is permanent and compute is ephemeral. Currently, while the Control Plane API exists, the underlying data stores (PostgreSQL, Qdrant, MinIO) and messaging backbone (NATS) need a unified production-ready deployment strategy on the Contabo VPS. This is essential for the "live semantic memory sync" where workers offload state before destruction.

## Decision
1.  **Hub & Spoke Architecture**:
    *   **The Hub (Supabase)**: Managed PostgreSQL for Workflows, Tasks, and AgentLogs. Leverages Supabase Real-time for instant dashboard updates.
    *   **The Memory Bank (Contabo)**: Self-hosted Qdrant (Vector), MinIO (Object), and NATS (Messaging) on the permanent VPS.
    *   **The Fleet (Vast.ai)**: Ephemeral high-compute workers.
2.  **Containerized Core (Contabo)**: Deploy Qdrant, MinIO, and NATS using Docker Compose. The `control-plane` API also runs here.
3.  **Persistence Strategy**:
    *   Relational state is managed by Supabase.
    *   Vector snapshots and project artifacts are synced to the Contabo MinIO/Qdrant during worker teardown.
4.  **Security**:
    *   Contabo services use authenticated tokens and secure Docker networking.
    *   Supabase connection uses SSL-enforced PostgreSQL strings.

## Consequences
*   **Pros**: Centralized state management. Reliable worker-to-core synchronization. Scalable infrastructure for multiple simultaneous projects.
*   **Cons**: Managed complexity of self-hosting object storage and vector databases.
