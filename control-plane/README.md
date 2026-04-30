# AlphaConsole Control Plane

The permanent "Brain" of the AlphaConsole platform. Handles orchestration, user management, and worker lifecycle.

## Getting Started

1.  **Environment Setup:**
    Create a `.env` file based on the config:
    ```env
    DATABASE_URL=postgresql://user:pass@supabase_host:5432/db
    NATS_URL=nats://your-contabo-ip:4222
    VAST_API_KEY=your_vast_key
    ```

2.  **Installation:**
    ```bash
    pip install poetry
    poetry install
    ```

3.  **Run:**
    ```bash
    uvicorn app.main:app --reload --port 8000
    ```

## Structure
- `app/api`: Endpoints for Dashboard and Workers.
- `app/core`: Security, Config, and Logging.
- `app/db`: Database models and session management.
- `app/services`: Orchestration logic (Vast.ai, NATS, Memory).
