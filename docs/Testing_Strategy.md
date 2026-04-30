# AlphaConsole Testing Strategy

This document outlines the testing tiers and quality assurance processes for AlphaConsole.

## 1. Unit & Integration Tests
*   **Control Plane (Python/FastAPI):** Managed via `pytest`. Focuses on API reliability, DB schema integrity, and NATS message formatting.
*   **Worker Runtime (Go):** Managed via `go test`. Focuses on concurrency, shell pool management, and system resource tracking.
*   **Agents (Python):** Individual tool validation and prompt integrity checks.

## 2. Feature Tests
Feature tests verify specific platform capabilities:
*   **Provisioning Logic:** End-to-end verification of Vast.ai offer filtering and human-gate approval.
*   **Hydration Accuracy:** Ensures that the JSON manifest correctly configures a shell's role and toolset.
*   **Memory RAG:** Validates that the Memory Agent returns the correct semantic context for a given query.

## 3. Full System Tests (E2E)
*   **Technology:** Playwright (Node.js).
*   **Workflow:**
    1.  Provision Instance.
    2.  Upload Project Intake.
    3.  Generate Plan.
    4.  Approve Plan.
    5.  Verify Parallel Task Completion.
    6.  Teardown Instance.

## 4. Documentation Quality (MkDocs)
The documentation site is automatically verified for broken links and metadata consistency during the build process.
