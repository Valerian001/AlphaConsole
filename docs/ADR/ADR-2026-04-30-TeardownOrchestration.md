# ADR-2026-04-30-TeardownOrchestration: Go Runtime Teardown & Pool Optimization

## Status
Approved

## Context
The "Gap Analysis" identified that the Go worker-runtime lacks robust teardown orchestration and uses a static pool size. The `Instance_Lifecycle_Specs.md` requires a "Self-Destruct Signal" that triggers database and vector backups before instance destruction. Additionally, the agent pool should scale dynamically based on hardware constraints to maximize throughput.

## Decision
1.  **Graceful Shutdown**: Implement a signal handler for `SIGINT` and `SIGTERM` in `main.go` that triggers a new `Teardown()` sequence.
2.  **Teardown Sequence**: The sequence will:
    *   Export a PostgreSQL dump (`pg_dump`).
    *   Trigger a Qdrant snapshot export.
    *   Upload all state artifacts to the remote object store (Contabo-hosted MinIO).
    *   Publish a `worker.teardown.complete` message to NATS.
3.  **Dynamic Pool Scaling**: Replace the hardcoded pool size (5) with a dynamic calculation based on available CPU cores and RAM. 
    *   Formula: `min(NumCPU, TotalRAM / 2GB)`.
4.  **Shell Hydration**: Implement the `HydrateShell` method in `WorkerRuntime` to write the `runtime_manifest.json` to the agent's workspace before execution.

## Consequences
*   **Pros**: Zero data loss during ephemeral instance destruction. Optimal resource utilization on various Vast.ai hardware offers.
*   **Cons**: Shutdown time increases slightly due to backup operations.
