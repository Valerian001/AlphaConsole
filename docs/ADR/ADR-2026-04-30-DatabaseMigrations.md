# ADR-2026-04-30-DatabaseMigrations: Alembic Migration System

## Status
Approved

## Context
The "Gap Analysis" identified that while the database schema is defined in documentation, it is not yet implemented in the codebase. There is no migration system in place for the PostgreSQL relational state.

## Decision
1.  **Migration Tool**: Use **Alembic** as the primary migration tool for the Python Control Plane.
2.  **ORM**: Use **SQLAlchemy** (async) for defining data models.
3.  **Schema Implementation**: Implement the following tables as defined in `Database_Schema_Specs.md`:
    *   `workflows`
    *   `tasks`
    *   `agent_logs`
4.  **Auto-Generation**: Configure Alembic's `env.py` to support auto-generating migrations from SQLAlchemy models.
5.  **Integration**: Ensure the `control-plane` can run migrations on startup or via a dedicated script.

## Consequences
*   **Pros**: Version-controlled database schema. "Fail-fast" schema validation. Consistent environments across local and production.
*   **Cons**: Slight overhead in managing migration files.
