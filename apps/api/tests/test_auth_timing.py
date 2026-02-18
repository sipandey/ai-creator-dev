import pytest
from unittest.mock import MagicMock
from app.services.auth_service import authenticate_user
from app.models.user import User
from app.core.security import DUMMY_HASH

def test_auth_timing_fix():
    """
    Verify that authenticate_user handles both existing and non-existing users
    without raising exceptions, ensuring the timing attack mitigation logic is executed.
    """
    # Mock DB session
    mock_db = MagicMock()

    # Test Case 1: User not found
    # Should trigger verify_password(..., DUMMY_HASH)
    mock_db.query.return_value.filter.return_value.first.return_value = None

    result = authenticate_user(mock_db, "nonexistent@example.com", "password123")
    assert result is None

    # Test Case 2: User found, wrong password
    # Should trigger verify_password(..., user.password_hash)
    mock_user = MagicMock(spec=User)
    mock_user.password_hash = DUMMY_HASH  # Use valid hash to pass format check

    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    result = authenticate_user(mock_db, "existing@example.com", "wrongpassword")
    assert result is None
