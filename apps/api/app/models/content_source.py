from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class ContentSource(Base):
    __tablename__ = "content_sources"
    
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    source_url = Column(String(500), nullable=True)  # For video URLs
    source_type = Column(String(50), nullable=False, index=True)  # 'video', 'text', 'manual'
    platform = Column(String(50), nullable=True)  # 'instagram', 'youtube', 'tiktok'
    content_data = Column(JSON, nullable=True)  # Extracted content (transcripts, metadata)
    confidence_contribution = Column(Float, default=0.0)
    processed_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    creator = relationship("User", back_populates="content_sources")