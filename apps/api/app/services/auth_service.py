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

    # Always perform password verification to prevent timing attacks
    if user:
        if verify_password(password, user.password_hash):
            return user
    else:
        # User not found, verify against dummy hash
        verify_password(password, DUMMY_HASH)

    return None
