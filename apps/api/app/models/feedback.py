from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from app.core.database import Base

class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    target: Mapped[str] = mapped_column(String)  
    # "script" | "strategy"

    feedback_type: Mapped[str] = mapped_column(String)
    signal: Mapped[str] = mapped_column(String)
    comment: Mapped[Optional[str]] = mapped_column(Text)
    
    # Add back_populates relationship
    user = relationship("User", back_populates="feedback")