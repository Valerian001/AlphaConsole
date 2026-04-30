# ADR-2026-04-30-ProductionReadiness: Backend Configuration & Software Stack Sync

## Status
Approved

## Context
An automated system audit identified missing production-critical configuration fields in `config.py` and a missing Python version requirement in `pyproject.toml`. These gaps prevent the system from being "Live Ready" and can lead to runtime failures if dependencies are mismatched.

## Decision
1.  **Software Stack**: Add `requires-python = ">=3.12"` to `control-plane/pyproject.toml` to ensure compatibility with modern Python features used in the codebase.
2.  **Configuration Schema**: 
    *   Add `QDRANT_URL`, `MINIO_ENDPOINT`, and `OLLAMA_BASE_URL` to the `Settings` class in `control-plane/app/core/config.py`.
    *   Make `DATABASE_URL` and `VAST_API_KEY` mandatory (remove `Optional`) for production environments to enforce a "fail-fast" policy.
3.  **Default Values**: Provide sensible defaults for local development but ensure they can be overridden via environment variables.

## Consequences
*   **Pros**: Increased system stability. Clearer infrastructure requirements for deployment. Compliance with automated audit rules.
*   **Cons**: None.
