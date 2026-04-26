# Instance Lifecycle & Provisioning Specification

This document defines the automated strategy for spinning up, initializing, and destroying ephemeral Vast.ai instances to maximize cost efficiency while ensuring data persistence.

---

## 1. Provisioning Flow (Spin-Up)

Instances are provisioned on-demand using the **Vast.ai CLI**.

### 1.1 Instance Selection Criteria
*   **GPU:** 1x RTX 4090 (24GB VRAM)
*   **CPU:** > 16 Cores
*   **RAM:** > 64GB (Prefer 128GB+)
*   **Image:** `nvidia/cuda:12.1.1-devel-ubuntu22.04` (or custom AgentOps base image)

### 1.2 Provisioning Command (Example)
```bash
vastai create instance <ID> \
  --image agentops/worker-base:latest \
  --disk 100 \
  --onstart "bash /root/init_system.sh"
```

---

## 2. System Initialization (Bootstrap)

Upon start, the `init_system.sh` script executes the following:

1.  **Environment Sync:** Pulls latest secrets and task context from the remote **Control Plane**.
2.  **Docker Orchestration:** 
    *   `docker-compose up -d`
    *   Verifies health of NATS, Postgres, and Ollama.
3.  **Model Loading:** Triggers `ollama pull qwen3.6` (or loads from a local cache volume if available).
4.  **Ready Signal:** Publishes a `worker.ready` message to the NATS backbone to signal availability for tasks.

---

## 3. Objective Monitoring (Execution)

The **Go Runtime** monitors the task queue via NATS.

*   **Active State:** Instance remains alive as long as there are "In Progress" tasks assigned to its `worker_id`.
*   **Idle Timeout:** If no tasks are received for **15 minutes**, the instance enters "Pre-Teardown" mode.

---

## 4. Persistence & Teardown (Spin-Down)

Before destruction, all state must be offloaded to ensure no data loss.

### 4.1 "Objective Accomplished" Trigger
A task is considered complete when:
1.  All agent stages (Planner -> Reviewer -> Developer -> Tester) report `SUCCESS`.
2.  Final artifacts (code, reports) are uploaded to the **Contabo-hosted MinIO**.
3.  The `agent_logs` and `task_results` are synced to **Supabase**.

### 4.2 Teardown Sequence
1.  **State Sync:** `pg_dump` and Qdrant snapshot upload to remote storage.
2.  **Artifact Verification:** Confirm all files in local MinIO are mirrored to the Remote Object Store.
3.  **Self-Destruct Signal:** Worker sends `worker.teardown.complete` to the Control Plane.
4.  **CLI Destroy:** Control Plane executes `vastai destroy instance <ID>`.

---

## 5. Cost Efficiency Metrics

| Action | Target Duration | Cost Impact |
| :--- | :--- | :--- |
| **Spin-up & Init** | < 5 Minutes | ~ $0.04 |
| **Model Load** | < 3 Minutes | ~ $0.02 |
| **Active Execution** | Variable | $0.44/hr |
| **Teardown & Sync** | < 2 Minutes | ~ $0.01 |

**Total Overhead per Lifecycle:** ~$0.10 + Execution Time.
