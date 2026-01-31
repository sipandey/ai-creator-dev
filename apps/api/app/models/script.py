from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class ScriptStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    FILMED = "FILMED"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"

class Script(Base):
    __tablename__ = "scripts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic = Column(String, nullable=False)
    script_json = Column(JSON, nullable=False)
    status = Column(String, default=ScriptStatus.DRAFT)
    performance_data = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    creator = relationship("User", back_populates="scripts")
