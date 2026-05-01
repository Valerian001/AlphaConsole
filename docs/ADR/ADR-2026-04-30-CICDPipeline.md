# ADR-2026-04-30-CICDPipeline: Automated Docker Builds and Deployment

## Status
Accepted

## Context
To ensure consistent deployments and live readiness, the Alpha system requires an automated CI/CD pipeline. Currently, Docker builds are manual, and there is no standardized registry for images used by the Contabo Control Plane and Vast.ai workers.

## Decision
1.  **Registry**: Use Docker Hub (`valerian001/alpha`) as the central repository for all system images.
2.  **Pipeline**: Implement **GitHub Actions** with a mandatory "Test-First" policy.
    *   **Trigger**: Push to the `main` branch.
    *   **Phase 1 (Test)**: Execute all Python (pytest) and Go (go test) suites. Any failure blocks the build.
    *   **Phase 2 (Build & Push)**: 
        *   `valerian001/alpha:control-plane`: The FastAPI brain.
        *   `valerian001/alpha:worker-runtime`: The Go supervisor.
3.  **Versioning**: 
    *   `latest` tag for the current production state.
    *   `sha-{GITHUB_SHA}` for granular rollback capability.
4.  **Security**: Store Docker Hub credentials (`DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`) as GitHub Repository Secrets.

## Consequences
*   **Pros**: Eliminated "works on my machine" issues. Standardized images for Vast.ai worker initialization. Faster deployment to Contabo via `docker-compose pull`.
*   **Cons**: Slight increase in build time on GitHub runners.
