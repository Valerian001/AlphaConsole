from core.base_shell import BaseAgentShell
import time
import json

class ReviewerAgent(BaseAgentShell):
    """
    The platform's quality core and fleet dispatcher.
    Analyzes plans and coordinates the 1:1 parallel execution.
    """
    
    def run(self):
        self.log("Reviewer Agent active. Auditing Implementation Plan...")
        
        # 1. Load the proposed plan from the Planner
        plan = self.manifest.get("proposed_plan", {})
        self.log(f"Reviewing Plan: {plan.get('adr_id')}")

        # 2. Perform Architecture & Quality Audit
        is_valid = self._audit_plan(plan)
        
        if not is_valid:
            self.log("CRITIQUE: Plan violates security constraints. Triggering RECYCLE loop.")
            # Emit RECYCLE result for Go supervisor
            self.finish({
                "status": "RECYCLE",
                "feedback": "Architecture violates VRAM constraints. Please optimize memory usage."
            })

        # 3. Handle Human-in-the-Loop Gate
        if self.manifest.get("require_human_approval", True):
            self.log("Plan Validated. Awaiting Human Approval via Dashboard...")
            self.finish({"status": "AWAITING_HUMAN"})

        # 4. Parallel Dispatch (1:1 Task Mapping)
        self.log("Dispatching fleet for parallel execution...")
        tasks = plan.get("milestones", [])
        self._dispatch_tasks(tasks)
        
        self.finish({"status": "SUCCESS", "task_count": len(tasks)})

    def _audit_plan(self, plan):
        """Simulates automated critique logic."""
        time.sleep(2)
        return True # Default to pass for initial integration

    def _dispatch_tasks(self, tasks):
        """Sends task assignments to the Go Runtime via NATS bridge."""
        for task in tasks:
            self.log(f"Assigning {task['name']} to {task['role']} shell.")
            # Dispatch logic: publish to task.{role}.assigned
            time.sleep(0.5)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python reviewer_agent.py <manifest_path>")
        sys.exit(1)
        
    agent = ReviewerAgent(sys.argv[1])
    agent.run()
