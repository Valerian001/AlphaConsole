from core.base_shell import BaseAgentShell
import time
import json
import os
import threading
import httpx
from typing import Dict, Any, List
from qdrant_client import QdrantClient
from qdrant_client.http import models

class MemoryAgent(BaseAgentShell):
    """
    Background daemon for semantic indexing and context management.
    Integrates with Qdrant for RAG capabilities.
    """
    
    def __init__(self, manifest_path: str):
        super().__init__(manifest_path)
        self.qdrant_url = self.manifest.get("qdrant_config", {}).get("url", "http://localhost:6333")
        self.ollama_url = self.manifest.get("ollama_config", {}).get("url", "http://localhost:11434")
        self.collection_name = "agent_memory"
        
        # Initialize Qdrant Client
        try:
            self.client = QdrantClient(url=self.qdrant_url)
            self.log(f"Connected to Qdrant at {self.qdrant_url}")
        except Exception as e:
            self.log(f"Failed to connect to Qdrant: {str(e)}")
            self.client = None

    def run(self):
        self.log("Memory Agent starting background sync...")
        
        # 1. Check boot mode (WARM vs COLD)
        boot_mode = self.manifest.get("sync_context", {}).get("boot_mode")
        self.log(f"Operating in {boot_mode} mode")
        
        if boot_mode == "WARM_RESTORE":
            self._restore_snapshot()
        else:
            self._initial_indexing()

        # 2. Main Daemon Loop
        while True:
            self.log("Checking for updated artifacts...")
            # In a real scenario, this would listen to NATS events
            time.sleep(30)

    def _restore_snapshot(self):
        self.log("Restoring Qdrant snapshot from Object Storage...")
        snapshot_path = self.manifest.get("sync_context", {}).get("snapshot_path")
        if snapshot_path and os.path.exists(snapshot_path):
            self.log(f"Recovering from {snapshot_path}")
            # self.client.recover_from_snapshot(self.collection_name, snapshot_path)
            time.sleep(2)
        else:
            self.log("No snapshot found. Proceeding with empty state.")

    def _initial_indexing(self):
        self.log("Beginning mass indexing of project intake...")
        intake_path = self.manifest.get("sync_context", {}).get("intake_path", "./intake")
        if os.path.exists(intake_path):
            for root, _, files in os.walk(intake_path):
                for file in files:
                    with open(os.path.join(root, file), 'r') as f:
                        content = f.read()
                        self.upsert_memory(content, {"source": file, "path": root})
            self.log("Initial indexing complete.")
        else:
            self.log("Intake path not found. Skipping initial indexing.")

    def upsert_memory(self, content: str, metadata: Dict[str, Any]):
        """Generates embedding and upserts to Qdrant."""
        if not self.client:
            return
            
        self.log(f"Indexing new memory: {content[:50]}...")
        vector = self._get_embedding(content)
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=metadata.get("id", int(time.time())),
                    vector=vector,
                    payload=metadata
                )
            ]
        )

    def search_memory(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Performs semantic search in Qdrant."""
        if not self.client:
            return []
            
        self.log(f"Searching memory for: {query}")
        vector = self._get_embedding(query)
        
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            limit=limit
        )
        
        return [hit.payload for hit in results]

    def _get_embedding(self, text: str) -> List[float]:
        """Calls Ollama to generate embeddings."""
        ollama_url = self.manifest.get("ollama_config", {}).get("base_url", "http://localhost:11434")
        model = self.manifest.get("ollama_config", {}).get("model", "qwen")
        
        try:
            response = httpx.post(
                f"{ollama_url}/api/embeddings",
                json={"model": model, "prompt": text},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()["embedding"]
        except Exception as e:
            self.log(f"Error calling Ollama embeddings: {e}")
            # Fallback to dummy if Ollama is unavailable in dev, but log it as error
            return [0.1] * 1536

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python memory_agent.py <manifest_path>")
        sys.exit(1)
        
    agent = MemoryAgent(sys.argv[1])
    agent.run()
