from sqlalchemy import Column, String, DateTime, JSON, Enum
from sqlalchemy.sql import func
import enum
from app.db.session import Base

class ObjectiveStatus(str, enum.Enum):
    INTAKE = "INTAKE"
    PLANNING = "PLANNING"
    REVIEW = "REVIEW"
    APPROVED = "APPROVED"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Objective(Base):
    __tablename__ = "objectives"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=True)
    description = Column(String, nullable=False)
    status = Column(Enum(ObjectiveStatus), default=ObjectiveStatus.INTAKE)
    
    # Storage paths
    intake_bucket = Column(String, nullable=True)
    qdrant_collection = Column(String, nullable=True)
    
    # Metadata
    manifest = Column(JSON, nullable=True) # The Implementation Plan / ADR
    config = Column(JSON, nullable=True)   # Project specific settings
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
