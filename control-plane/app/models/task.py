from sqlalchemy import Column, String, DateTime, JSON, Enum, ForeignKey
from sqlalchemy.sql import func
import enum
from app.db.session import Base

class TaskStatus(str, enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    RECYCLED = "RECYCLED"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)
    objective_id = Column(String, ForeignKey("objectives.id"), nullable=False)
    
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    
    agent_role = Column(String, nullable=False) # DEVELOPER, TESTER, etc.
    agent_id = Column(String, nullable=True)   # The specific shell ID assigned
    
    # Context
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
