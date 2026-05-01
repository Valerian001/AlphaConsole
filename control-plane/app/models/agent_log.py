from sqlalchemy import Column, String, Text, JSON, DateTime, ForeignKey, BigInteger, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.session import Base

class AgentLog(Base):
    __tablename__ = "agent_logs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"))
    agent_type = Column(String(50))
    content = Column(Text)
    metadata_json = Column(JSON, name="metadata") # Using metadata_json to avoid conflict with SQLAlchemy metadata
    trace_id = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
