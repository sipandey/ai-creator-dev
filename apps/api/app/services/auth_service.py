from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password, verify_password, DUMMY_HASH

def create_user(db: Session, email: str, password: str, creator_type: str):
    user = User(
        email=email,
        password_hash=hash_password(password),
        creator_type=creator_type,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    # Use real password hash if user exists, otherwise use dummy hash
    # This ensures verify_password is always called, mitigating timing attacks
    password_hash = user.password_hash if user else DUMMY_HASH

    if not verify_password(password, password_hash):
        return None

    # If we used the dummy hash (user was None), we must still return None
    if not user:
        return None

    return user
