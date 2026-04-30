# Memory Agent Initialization Specification

This document defines the technical "Hydration" process and runtime context for the **Memory Agent**, the semantic backbone responsible for knowledge persistence and context retrieval.

---

## 1. Initialization Manifest (JSON Payload)

When the Go Runtime hydrates a shell into a Memory Agent, it injects the following `runtime_manifest.json`:

```json
{
  "agent_id": "mem-omega-01",
  "role": "MEMORY_MANAGER",
  "sync_context": {
    "project_id": "proj_98231",
    "remote_store": "https://contabo-minio.alpha.com",
    "bucket_name": "alpha-memory-snapshots",
    "boot_mode": "WARM_RESTORE" | "COLD_INDEX"
  },
  "vector_config": {
    "collection_name": "memory_proj_98231",
    "embedding_model": "nomic-embed-text",
    "vector_size": 768
  },
  "capabilities": [
    "VECTOR_DB_SYNC",
    "SEMANTIC_SEARCH",
    "CONTEXT_PRUNING",
    "ARTIFACT_INDEXING"
  ],
  "sandbox_config": {
    "memory_limit": "2GB",
    "cpu_shares": 512,
    "priority": "BACKGROUND"
  }
}
```

---

## 2. Toolset Configuration (Injection)

The Memory Agent is initialized with a "Context Engineering" toolset bridge:

| Tool Name | Scope | Description |
| :--- | :--- | :--- |
| `sync_remote_snapshot` | `CONTABO_S3` | Handles the upload/download of Qdrant snapshots and project code bundles. |
| `query_relevant_context` | `QDRANT` | Provides RAG context to other agents by performing high-speed vector searches. |
| `index_new_artifacts` | `MINIO` | Automatically converts new files, logs, and decisions into semantic embeddings. |
| `prune_memory_nodes` | `QDRANT` | Deletes vectors and metadata associated with irrelevant or deleted project assets. |
| `broadcast_context` | `NATS` | Publishes high-level context updates to the `memory.update` stream. |

---

## 3. Initialization Logic (Sequence)

1.  **Remote Handshake:**
    *   Authenticates with the Contabo MinIO using the user's encrypted credentials.
    *   Checks for the existence of a `last_known_snapshot.qdrant`.
2.  **State Hydration:**
    *   **If WARM:** Downloads and restores the Qdrant snapshot into the local worker database.
    *   **If COLD:** Downloads the initial project intake bundle and begins the mass-embedding process.
3.  **NATS Subscription:**
    *   Subscribes to `agent.*.output` and `code.commit` streams to monitor for data that needs indexing.
4.  **Operational Pulse:**
    *   Publishes `memory.ready` and enters a background daemon mode to serve context requests from the fleet.

---

## 4. Resource Allocation (Sandbox)

*   **Runtime:** Python 3.12 (Low-resource Background Process).
*   **Memory Limit:** 2GB RAM.
*   **Storage:** Direct access to the local Qdrant persistence layer.
*   **Networking:** Allowed to communicate with Contabo MinIO and local Qdrant/Ollama endpoints.
