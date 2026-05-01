from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.objective import Objective, ObjectiveStatus
from app.services.nats_svc import nats_service
import uuid

router = APIRouter(prefix="/objectives", tags=["Project Objectives"])

@router.post("/")
async def create_objective(description: str, db: Session = Depends(get_db)):
    """
    Creates a new project objective and triggers the INTAKE phase.
    """
    obj_id = str(uuid.uuid4())
    new_obj = Objective(
        id=obj_id,
        description=description,
        status=ObjectiveStatus.INTAKE
    )
    
    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    
    # Trigger NATS event for Memory Agent to start intake indexing
    await nats_service.publish_task("agent.task.create", {
        "objective_id": obj_id,
        "description": description
    })
    
    return new_obj

@router.get("/")
async def list_objectives(db: Session = Depends(get_db)):
    return db.query(Objective).all()

@router.get("/{obj_id}")
async def get_objective(obj_id: str, db: Session = Depends(get_db)):
    obj = db.query(Objective).filter(Objective.id == obj_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Objective not found")
    return obj

@router.post("/{obj_id}/start-planning")
async def start_planning(obj_id: str, db: Session = Depends(get_db)):
    """
    Transitions the objective to the PLANNING phase and triggers the Planner Agent.
    """
    obj = db.query(Objective).filter(Objective.id == obj_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Objective not found")
    
    obj.status = ObjectiveStatus.PLANNING
    db.commit()
    
    # Trigger NATS event for Planner Agent
    await nats_service.publish_task("agent.worker.planner.exec", {
        "objective_id": obj_id,
        "context": obj.description
    })
    
    return {"status": "planning_started", "objective_id": obj_id}
