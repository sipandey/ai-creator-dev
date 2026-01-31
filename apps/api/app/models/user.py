from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    creator_type = Column(String, nullable=False)  # 'NEW' or 'EXISTING'
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    persona = relationship("CreatorPersona", back_populates="creator", uselist=False)
    content_sources = relationship("ContentSource", back_populates="creator")
    feedback = relationship("Feedback", back_populates="user")
    preferences = relationship("Preference", back_populates="user")
    scripts = relationship("Script", back_populates="creator")
    strategies = relationship("ContentStrategy", back_populates="creator")