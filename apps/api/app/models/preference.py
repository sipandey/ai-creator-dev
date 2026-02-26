from sqlalchemy import ForeignKey, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Preference(Base):
    __tablename__ = "preferences"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    key: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)   # hard | soft
    value: Mapped[str] = mapped_column(String)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Add back_populates relationship
    user = relationship("User", back_populates="preferences")