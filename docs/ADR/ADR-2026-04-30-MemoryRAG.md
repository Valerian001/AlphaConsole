# ADR-2026-04-30-MemoryRAG: Semantic Memory Integration with Qdrant

## Status
Approved

## Context
The current `MemoryAgent` implementation is a placeholder that simulates background indexing. To provide actual multi-agent context management, it must be integrated with the Qdrant vector database as defined in the `Database_Schema_Specs.md`.

## Decision
1.  **Library**: Use `qdrant-client` for interacting with the vector database.
2.  **Collection**: Target the `agent_memory` collection.
3.  **Embeddings**: Implement a stub for embedding generation (using `httpx` to call the Ollama service defined in `OLLAMA_BASE_URL`).
4.  **Distance Metric**: Use `Cosine Similarity`.
5.  **Functionality**:
    *   **Indexing**: Implement `_initial_indexing()` to walk the intake bucket and upsert embeddings.
    *   **Search**: Implement a NATS-triggered search method (routed via the shell) to allow other agents to query memory.
    *   **Restoration**: Implement `_restore_snapshot()` using the MinIO client to pull the latest snapshot before Qdrant startup.

## Consequences
*   **Pros**: Enables actual semantic recall for agents. Improves cross-task reasoning.
*   **Cons**: Increases agent startup time due to initial indexing and snapshot restoration.
