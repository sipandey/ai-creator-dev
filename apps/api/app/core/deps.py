from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from jose import jwt

from app.core.database import SessionLocal
from app.models.user import User
from app.core.auth import SECRET_KEY, ALGORITHM

security = HTTPBearer()

# ✅ FIRST: define get_db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ THEN: define get_current_user
def get_current_user(
    token=Depends(security),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
