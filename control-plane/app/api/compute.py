from fastapi import APIRouter, HTTPException, Depends
from app.services.vast_svc import vast_orchestrator
from typing import List, Dict

router = APIRouter(prefix="/compute", tags=["Compute Orchestration"])

@router.get("/offers")
async def get_vast_offers():
    """
    Returns a filtered list of Vast.ai GPU instances matching 
    the RTX 4090 requirement.
    """
    offers = vast_orchestrator.filter_instances()
    if not offers:
        raise HTTPException(status_code=503, detail="No matching Vast.ai offers found.")
    return offers

@router.post("/provision")
async def provision_instance(offer_id: int):
    """
    Provision a specific Vast.ai instance based on user selection.
    This is the 'Human-in-the-loop Pricing Gate'.
    """
    result = vast_orchestrator.create_instance(offer_id)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to provision instance on Vast.ai.")
    return {"status": "provisioning", "details": result}

@router.get("/instances")
async def list_instances():
    """Returns all active compute instances."""
    return vast_orchestrator.get_instances()

@router.delete("/instances/{instance_id}")
async def terminate_instance(instance_id: int):
    """Terminates an active compute instance."""
    success = vast_orchestrator.destroy_instance(instance_id)
    if not success:
        raise HTTPException(status_code=404, detail="Instance not found or could not be destroyed.")
    return {"status": "terminated"}
