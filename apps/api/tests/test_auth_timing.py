import pytest
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.core.database import Base

# Import ALL models
from app.models.user import User
from app.models.persona import CreatorPersona
from app.models.feedback import Feedback
from app.models.preference import Preference
from app.models.content_source import ContentSource
try:
    from app.models.script import Script
except ImportError:
    pass
try:
    from app.models.strategy import ContentStrategy
except ImportError:
    pass

from app.services.auth_service import authenticate_user, create_user

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_auth_timing_mitigation(db_session):
    """
    Test to verify that timing attack mitigation is working.
    Expected: Authenticating an existing user (wrong password) and a non-existing user
    should take approximately the same time.
    """
    email = "timing_test@example.com"
    password = "secure_password_123"
    create_user(db_session, email, password, "creator")

    # Warmup
    authenticate_user(db_session, email, "wrong_password")
    authenticate_user(db_session, "non_existent@example.com", "any_password")

    # Measure time for existing user
    start_time = time.perf_counter()
    authenticate_user(db_session, email, "wrong_password")
    existing_user_time = time.perf_counter() - start_time

    # Measure time for non-existing user
    start_time = time.perf_counter()
    authenticate_user(db_session, "non_existent@example.com", "any_password")
    non_existing_user_time = time.perf_counter() - start_time

    print(f"\nExisting user time: {existing_user_time:.6f}s")
    print(f"Non-existing user time: {non_existing_user_time:.6f}s")

    diff = existing_user_time - non_existing_user_time
    ratio = existing_user_time / non_existing_user_time if non_existing_user_time > 0 else 1.0

    print(f"Difference: {diff:.6f}s")
    print(f"Ratio: {ratio:.2f}x")

    # Assert that the timing is consistent (mitigated)
    # We allow some variance, but it shouldn't be orders of magnitude different
    assert 0.5 < ratio < 1.5, f"Timing difference detected! Ratio: {ratio:.2f}"
    assert abs(diff) < 0.1, f"Timing difference too large! Diff: {diff:.6f}s"

def test_auth_functionality(db_session):
    """
    Verify that authentication still works correctly.
    """
    email = "valid_user@example.com"
    password = "valid_password"
    create_user(db_session, email, password, "creator")

    # 1. Successful login
    user = authenticate_user(db_session, email, password)
    assert user is not None
    assert user.email == email

    # 2. Wrong password
    user = authenticate_user(db_session, email, "wrong_password")
    assert user is None

    # 3. User not found
    user = authenticate_user(db_session, "invalid@example.com", "password")
    assert user is None
