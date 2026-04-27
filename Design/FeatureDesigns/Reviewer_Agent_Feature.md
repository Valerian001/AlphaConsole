# Feature Design: Reviewer Agent (The Orchestration Gatekeeper)

The Reviewer Agent acts as the quality assurance and dispatch center for AlphaConsole. It manages the iterative loop between planning and execution.

---

## 1. Core Logic: The Agile Loop

The workflow follows a recursive refinement pattern:

1.  **Initial Plan:** The **Planner** generates an Implementation Plan.
2.  **Internal Review (Planner ↔ Reviewer):**
    *   Reviewer analyzes the plan for technical gaps, security risks, and resource efficiency.
    *   If issues are found, it sends a `revision_request` back to the Planner.
    *   This loop repeats until the Reviewer issues a `technical_approval`.
3.  **Human Verification (Reviewer ↔ User):**
    *   The approved plan is presented to the User on the AlphaConsole.
    *   **User Feedback:** The User can approve or provide comments.
    *   **Recycle:** User comments are sent back to the **Planner**, restarting the Internal Review loop.
4.  **Dispatch:** Upon final User approval, the Reviewer identifies the best-suited executing agents (Developer, Tester, etc.) and dispatches the task.

---

## 2. Intelligence: Fleet Awareness

The Reviewer maintains a "Fleet Capability Matrix":
*   **Agent Directory:** Knows all active agents and their specializations.
*   **Load Balancing:** Checks agent health/load before dispatching.
*   **Security Context:** Ensures executing agents have the correct scope-based permissions for the plan's requirements.
*   **Repository Validation:** 
    *   Verifies if a GitHub repository is linked to the project.
    *   If missing (for new projects), the Reviewer **must** block the dispatch and request the URL from the User via the Human Gate.
    *   Enforces that the **Planner** only uses cloning/parsing tools and never attempts repo creation.

---

## 3. Visual Requirements (Mockup Integration)

*   **Iteration History:** A timeline showing how many "Roundtrips" occurred between Planner and Reviewer.
*   **Feedback Interface:** A prominent comment box on the Approval screen for the User to interact with the loop.
*   **Dispatch Animation:** A visual transition on the dashboard showing the Reviewer "broadcasting" the task to the execution fleet.

---

## 4. Interaction Patterns

*   **Direct Critique:** The User's comments are treated as "High Priority" constraints by the Planner.
*   **Conflict Resolution:** If the Planner cannot meet a Reviewer requirement, it must escalate with an "Impossible Constraint" report for the User to settle.
