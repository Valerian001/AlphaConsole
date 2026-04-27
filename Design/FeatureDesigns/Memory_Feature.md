# Feature Design: Memory Module

The Memory module manages the "Semantic Brain" of AlphaConsole, controlling how context is retrieved and persisted across tasks.

---

## 1. Core Logic
*   **Vector Collections:** Managing Qdrant collections organized by project or client.
*   **Context Injection:** Rules for how much "Short-term" vs "Long-term" memory is injected into an agent's prompt.
*   **Snapshots:** Managing the sync between ephemeral worker Qdrant instances and the permanent Contabo storage.

---

## 2. Visual Requirements
*   **Semantic Explorer:** A visual tool to browse vector "neighbors" and search through project context.
*   **Relevance Heatmap:** Visualizing which memories are being hit most frequently by the agents.
*   **Context Window Monitor:** Real-time visualization of how much of the LLM context is filled by memory retrieval.

---

## 3. Interaction Patterns
*   **Manual Pruning:** Deleting irrelevant or outdated memories to maintain high retrieval precision.
*   **Knowledge Injection:** Manually uploading documentation or code snippets directly into the semantic store.
