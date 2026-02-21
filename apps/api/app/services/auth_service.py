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

    # Use dummy hash if user not found to prevent timing attacks (user enumeration)
    # Always perform password verification to make timing consistent
    if user:
        pwd_hash = user.password_hash
    else:
        pwd_hash = DUMMY_HASH

    # verify_password performs bcrypt check which is slow (intentional)
    is_valid = verify_password(password, pwd_hash)

    if not user or not is_valid:
        return None

    return user
