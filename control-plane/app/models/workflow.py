from sqlalchemy import Column, String, JSON, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.session import Base

class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    definition = Column(JSON, nullable=False)  # List of stages and agent types
    created_at = Column(DateTime(timezone=True), server_default=func.now())
