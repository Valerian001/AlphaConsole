# Hardware & Infrastructure Specification

This document defines the hardware requirements for the AgentOps platform deployment on **Vast.ai**, optimized for running Qwen 3.6 and the polyglot worker stack.

---

## 1. Primary Compute: Vast.ai Instance

### 1.1 Recommended Configuration (GPU Dedicated)
Optimized for high-throughput multi-agent execution in the ZA region.
*   **Type:** Vast.ai #30468002 (Ubuntu 22.04 VM)
*   **GPU:** 1x NVIDIA RTX 4090 (24 GB VRAM)
*   **CPU:** AMD EPYC 7542 (32 Cores / 64 Threads)
*   **RAM:** 129 GB System RAM (DDR4)
*   **Storage:** 2TB Samsung 980 PRO NVMe (Shared/Container storage)
*   **Network:** 638 Mbps Symmetric Uplink/Downlink
*   **CUDA Support:** Max 12.9

---

## 2. Resource Allocation Matrix (Docker)

To prevent resource contention (ADR-034), these limits must be defined in `docker-compose.yml`.

| Service | CPU Reservation | RAM Limit | GPU Access | Priority |
| :--- | :--- | :--- | :--- | :--- |
| **Ollama (Qwen 3.6)** | 8 Cores | 64 GB* | Full (24GB VRAM) | **Critical** |
| **Go Runtime** | 4 Cores | 8 GB | No | High |
| **Python Worker Pool**| 8 Cores | 16 GB | No | Medium |
| **FastAPI Control** | 1 Core | 4 GB | No | Medium |
| **Qdrant Vector DB** | 4 Cores | 16 GB | No | High |
| **PostgreSQL** | 2 Cores | 8 GB | No | High |
| **Infrastructure (NATS/Redis)** | 1 Core | 4 GB | No | High |

*\*The high RAM limit (64GB) allows for offloading KV caches or running quantized model layers in system RAM if VRAM (24GB) is exceeded by large context windows.*

---

## 3. Storage & I/O Strategy (Ephemeral vs. Persistent)

Since Vast.ai instances are destroyed after objective completion, a **Hybrid Storage Strategy** is required.

### 3.1 Local High-Speed Storage (Ephemeral)
Used for active execution and low-latency DB operations.
*   **/opt/agentops/postgres/data**: Local NVMe (Fast I/O)
*   **/opt/agentops/qdrant/storage**: Local NVMe (Vector retrieval)
*   **/opt/agentops/minio/data**: Local NVMe (Active artifact staging)

### 3.2 Remote Persistent Storage (Canonical)
All state must be synced here before instance destruction (See `Instance_Lifecycle_Specs.md`).
*   **Database Master:** External PostgreSQL hosted on **Supabase**.
*   **Object Store:** **MinIO** instance hosted on **Contabo**.
*   **Vector Snapshots:** Remote storage via the same **Contabo-hosted MinIO** bucket.

---

## 4. Network Configuration (Vast.ai Ingress)

*   **Public Interface:** Access via Vast.ai Port Mapping (Direct Proxy).
*   **Ports:**
    *   `80/443`: Mapped to internal Nginx (HTTPS termination).
    *   `22`: Direct SSH to Instance.
*   **Note:** DigitalOcean VPC features are replaced by Docker-internal networking as Vast.ai instances are typically standalone.
*   **Private Interface (VPC):** All internal communication between Docker containers and any potential future horizontal nodes.
*   **Firewall Rules (UFW):**
    ```bash
    ufw default deny incoming
    ufw allow 80/tcp
    ufw allow 443/tcp
    ufw allow from <ADMIN_IP> to any port 22 proto tcp
    ```

---

## 5. OS Baseline

*   **Distribution:** Ubuntu 24.04 LTS
*   **Kernel:** Generic Linux with `nvidia-container-toolkit` and `nvidia-drivers-550+`.
*   **Optimization:** Enable Swap (16GB) on NVMe to prevent OOM kills during high-context LLM retrieval.
