from core.base_shell import BaseAgentShell
import time

class PlannerAgent(BaseAgentShell):
    """
    Architectural lead responsible for task decomposition and ADR generation.
    """
    
    def run(self):
        self.log("Planner Agent active. Analyzing requirements...")
        
        # 1. Access project context from manifest
        ctx = self.manifest.get("project_context", {})
        obj_desc = ctx.get("description", "No description provided.")
        feedback = self.manifest.get("previous_feedback")
        
        if feedback:
            self.log(f"REVISION MODE: Addressing feedback -> {feedback}")
        
        self.log(f"Goal: {obj_desc}")

        # 2. Simulate Architectural Reasoning
        self.log("Phase A: Ingesting Project Intake assets (PDF/Images)...")
        time.sleep(1)
        
        # 3. Output Plan
        plan = {
            "objective_name": "Auth Core Integration",
            "adr_id": "ADR-PROJ-001",
            "milestones": [
                {"name": "Setup DB Schema", "role": "DEVELOPER"},
                {"name": "Implement Middleware", "role": "DEVELOPER"},
                {"name": "Verify Security", "role": "TESTER"}
            ]
        }
        
        self.log(f"Plan Generated: {plan['objective_name']}")
        
        self.finish({"status": "SUCCESS", "plan": plan})

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python planner_agent.py <manifest_path>")
        sys.exit(1)
        
    agent = PlannerAgent(sys.argv[1])
    agent.run()
