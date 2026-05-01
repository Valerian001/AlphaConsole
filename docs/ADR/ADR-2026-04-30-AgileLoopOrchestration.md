# ADR-2026-04-30-AgileLoopOrchestration: Recursive Feedback Loop in Go Runtime

## Status
Accepted

## Context
The "Agile-Loop" is a recursive feedback cycle where the **Reviewer Agent** evaluates the output of the **Planner Agent**. If the Reviewer identifies architectural violations or resource overruns, it must trigger a "Recycle" event that sends feedback back to the Planner for a revised strategy. Currently, this coordination is manually handled or stubbed.

## Decision
1.  **Local Loop Execution**: To minimize latency and Control Plane overhead, the primary feedback loop will be orchestrated by the **Go Worker Runtime**.
2.  **Completion Signals**: 
    *   Agents will write a standardized `result_{agent_id}.json` file upon completion.
    *   The Go Runtime will monitor the agent process exit and immediately read this result.
3.  **Recycle Trigger**:
    *   If the result status is `RECYCLE`, the Go Runtime will capture the `feedback` field and automatically re-hydrate an idle shell as a **Planner**, passing the previous context plus the new feedback.
    *   The loop continues recursively until the Reviewer emits a `SUCCESS` or `AWAITING_HUMAN` status.
4.  **State Sync**: Every iteration of the loop is reported back to the Control Plane via the `agent.task.status.{id}` NATS subject.

## Consequences
*   **Pros**: Ultra-low latency feedback (no network round-trip to Control Plane needed for internal agent iteration). Robust handling of architectural constraints.
*   **Cons**: Increases complexity in the Go Runtime supervisor logic.
