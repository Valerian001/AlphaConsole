# Database & Memory Schema Specification

This document defines the data models for PostgreSQL (Relational State) and Qdrant (Semantic Memory).

---

## 1. PostgreSQL Schema (Relational State)

### 1.1 `Workflows` Table
Stores the blueprint for multi-stage agent tasks.
```sql
CREATE TABLE workflows (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    definition JSONB NOT NULL, -- List of stages and agent types
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 1.2 `Tasks` Table
Tracks the lifecycle of an individual execution.
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY,
    workflow_id UUID REFERENCES workflows(id),
    status VARCHAR(50) DEFAULT 'created', -- created, running, paused, completed, failed
    current_stage VARCHAR(100),
    context JSONB, -- Global task context shared between agents
    result JSONB,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 1.3 `AgentLogs` Table
Detailed structured logs for observability.
```sql
CREATE TABLE agent_logs (
    id BIGSERIAL PRIMARY KEY,
    task_id UUID REFERENCES tasks(id),
    agent_type VARCHAR(50),
    content TEXT,
    metadata JSONB,
    trace_id VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 2. Qdrant Schema (Semantic Memory)

### 2.1 Collection: `agent_memory`
Stores vector embeddings of past reasoning and project knowledge.
*   **Vector Size:** 1536 (Standard for many Qwen embeddings) or 1024 (depending on model).
*   **Distance Metric:** Cosine Similarity.
*   **Payload Fields:**
    *   `project_id`: UUID
    *   `agent_type`: string
    *   `source_task_id`: UUID
    *   `content_summary`: string
    *   `timestamp`: int (Unix)

---

## 3. Migration Strategy

*   **Python (FastAPI):** Use `Alembic` for declarative migrations.
*   **Go (Runtime):** Use `golang-migrate` for versioned SQL execution.
*   **Vector DB:** Qdrant collections are managed via a custom initialization script in the `Go Runtime` startup phase.
