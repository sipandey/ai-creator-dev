from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class CreatorPersona(Base):
    __tablename__ = "creator_persona"  # Keep existing table name for compatibility

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    persona_json = Column(JSON, nullable=False)
    confidence_score = Column(Float, nullable=True)
    source = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # New columns (added via migration)
    version = Column(String(10), default="v1")
    content_sources = Column(JSON, nullable=True)  # Track which sources contributed
    processing_metadata = Column(JSON, nullable=True)  # Store processing details

    # Relationships
    creator = relationship("User", back_populates="persona")