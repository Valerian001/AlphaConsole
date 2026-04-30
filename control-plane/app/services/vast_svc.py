import subprocess
import json
from typing import List, Dict, Optional
from app.core.config import settings

class VastOrchestrator:
    """
    Service to interact with the Vast.ai CLI for marketplace filtering 
    and instance lifecycle management as per ADR-2026-04-28.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.VAST_API_KEY
        
    def filter_instances(self) -> List[Dict]:
        """
        Queries Vast.ai for instances matching our Hardware Specs:
        - RTX 4090
        - 24GB VRAM
        - > 500Mbps Up/Down
        - > 16 CPU Cores
        """
        # Command: vastai search offers 'gpu_name==RTX_4090 gpu_ram>=24 inet_up>500 cpu_cores>=16'
        query = "gpu_name==RTX_4090 gpu_ram>=24 inet_up>500 cpu_cores>=16"
        cmd = ["vastai", "search", "offers", query, "--raw"]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            offers = json.loads(result.stdout)
            
            # Sort by price (dph - dollars per hour)
            sorted_offers = sorted(offers, key=lambda x: x.get('dph_total', 999))
            return sorted_offers
        except Exception as e:
            print(f"Error querying Vast.ai: {e}")
            return []

    def create_instance(self, offer_id: int, image: str = "nvidia/cuda:12.1.1-devel-ubuntu22.04"):
        """
        Spawns a new instance from a selected offer and injects the bootstrap script.
        """
        # vastai create instance <id> --image <image> --onstart-bundle <bootstrap_script>
        cmd = [
            "vastai", "create", "instance", str(offer_id),
            "--image", image,
            "--disk", "100" # 100GB Disk
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except Exception as e:
            print(f"Error creating Vast.ai instance: {e}")
            return None

    def get_instances(self) -> List[Dict]:
        """Returns all currently active instances."""
        cmd = ["vastai", "show", "instances", "--raw"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except:
            return []

    def destroy_instance(self, instance_id: int):
        """Terminates an instance."""
        cmd = ["vastai", "destroy", "instance", str(instance_id)]
        try:
            subprocess.run(cmd, check=True)
            return True
        except:
            return False

vast_orchestrator = VastOrchestrator()
