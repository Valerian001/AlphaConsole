from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.objective import Objective, ObjectiveStatus
from app.models.task import Task, TaskStatus
from app.services.nats_svc import nats_service
import uuid

router = APIRouter(prefix="/reviewer", tags=["Reviewer Orchestration"])

@router.post("/{obj_id}/approve")
async def approve_plan(obj_id: str, tasks_data: list, db: Session = Depends(get_db)):
    """
    User approves the implementation plan. 
    Reviewer dispatches the subtasks to the worker fleet.
    """
    obj = db.query(Objective).filter(Objective.id == obj_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Objective not found")
    
    obj.status = ObjectiveStatus.EXECUTING
    
    # Create individual tasks in the DB and publish to NATS
    for task_info in tasks_data:
        task_id = str(uuid.uuid4())
        new_task = Task(
            id=task_id,
            objective_id=obj_id,
            name=task_info["name"],
            description=task_info["description"],
            agent_role=task_info["role"],
            status=TaskStatus.PENDING
        )
        db.add(new_task)
        
        # Dispatch to NATS (1:1 Parallel model)
        await nats_service.publish_task(f"task.{task_info['role'].lower()}.assigned", {
            "task_id": task_id,
            "objective_id": obj_id,
            "name": task_info["name"],
            "description": task_info["description"]
        })
    
    db.commit()
    return {"status": "dispatched", "task_count": len(tasks_data)}
