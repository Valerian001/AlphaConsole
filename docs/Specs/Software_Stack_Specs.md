# Software Stack Specification

This document details the software versions, configurations, and integration patterns for the AgentOps platform.

---

## 1. Core Services Stack

| Component | Technology | Version | Key Configuration |
| :--- | :--- | :--- | :--- |
| **Control Plane** | FastAPI | 0.110+ | Python 3.12, Pydantic v2 |
| **Execution Runtime**| Go | 1.22+ | Modules enabled, Goroutine pools |
| **Messaging** | NATS | 2.10+ | JetStream enabled, Durable streams |
| **AI Inference** | Ollama | Latest | Qwen 3.6 (27B/72B) |
| **Primary DB** | PostgreSQL | 16.2 | JSONB for logs, WAL-G enabled |
| **Vector DB** | Qdrant | 1.8+ | HNSW indexing, gRPC enabled |
| **Object Store** | MinIO | Latest | Distributed mode (if scaling) |
| **Cache/Locking** | Redis | 7.2 | Redlock algorithm for concurrency |

---

## 2. Agent Worker Environment (Python)

To ensure consistency across various agent types (Planner, Developer, etc.), a standardized base image is used.
*   **Base Image:** `python:3.12-slim-bookworm`
*   **Core Libraries:**
    *   `langchain` / `langgraph` (Orchestration)
    *   `openai` / `ollama-python` (Inference client)
    *   `pydantic` (Data validation)
    *   `opentelemetry-sdk` (Tracing)
    *   `nats-py` (Messaging)

---

## 3. Communication Protocols

### 3.1 NATS Subject Hierarchy
All inter-service communication follows this pattern:
*   `agent.task.create`: New task submitted.
*   `agent.task.status.{id}`: Real-time status updates.
*   `agent.worker.{type}.exec`: Commands to specific worker pools.
*   `agent.worker.logs.{id}`: Streaming logs from agents.
*   `worker.teardown.complete`: Signal sent by runtime before instance destruction.

### 3.2 WebSocket Sync
*   **Endpoint:** `/ws/v1/sync`
*   **Payload:** JSON-formatted events mirroring NATS messages for dashboard reactivity.

---

## 4. Configuration Management

*   **Format:** YAML (Primary config) and `.env` (Secrets).
*   **Secret Injection:** Handled via Docker Secrets in production to prevent environment variable leakage in `docker inspect`.
