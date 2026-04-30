import json
import os
import sys
from typing import Dict, Any

class BaseAgentShell:
    """
    Standardized wrapper for AlphaConsole agents.
    Handles manifest loading, tool routing, and logging.
    """
    
    def __init__(self, manifest_path: str):
        self.manifest = self._load_manifest(manifest_path)
        self.role = self.manifest.get("role")
        self.agent_id = self.manifest.get("agent_id")
        
        print(f"Agent {self.agent_id} initialized as {self.role}")

    def _load_manifest(self, path: str) -> Dict[str, Any]:
        with open(path, 'r') as f:
            return json.load(f)

    def log(self, message: str):
        """Structured logging for real-time dashboard streaming."""
        log_entry = {
            "agent_id": self.agent_id,
            "role": self.role,
            "message": message,
            "timestamp": "iso_timestamp_here"
        }
        print(json.dumps(log_entry))

    def run(self):
        """Main execution loop (to be overridden by specific agents)."""
        raise NotImplementedError("Subclasses must implement run()")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python base_shell.py <manifest_path>")
        sys.exit(1)
        
    shell = BaseAgentShell(sys.argv[1])
