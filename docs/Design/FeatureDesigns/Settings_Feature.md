# Feature Design: Settings Module

The Settings module is the administrative hub for infrastructure, security, and global platform configurations.

---

## 1. Core Logic
*   **Infrastructure Keys:** Storing and encrypting API keys for Vast.ai, Supabase, and Contabo.
*   **Model Config:** Global defaults for Ollama (default quantization, default context length).
*   **User Management:** RBAC for human operators of AlphaConsole.

---

## 2. Visual Requirements
*   **Connectivity Dashboard:** Real-time health status of external providers (Vast.ai API status, Supabase connectivity).
*   **Budget & Usage:** Tracking costs accrued on Vast.ai per objective or project.
*   **Theme & UX:** Customizing the dashboard appearance (Obsidian Flow toggles).

---

## 3. Interaction Patterns
*   **Infrastructure Test:** A "Dry Run" button to verify provisioning of a Vast.ai instance and connection to Supabase in one click.
*   **Secret Rotation:** Automated cycling of platform-wide credentials.
