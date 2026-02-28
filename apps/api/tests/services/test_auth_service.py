import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from app.services.auth_service import create_user, authenticate_user
from app.models.user import User
from app.core.security import hash_password, verify_password, DUMMY_HASH

def test_authenticate_user_success():
    db_mock = MagicMock(spec=Session)
    mock_user = MagicMock(spec=User)
    mock_user.email = "test@example.com"
    mock_user.password_hash = hash_password("password123")

    # Mock query to return our mock user
    db_mock.query.return_value.filter.return_value.first.return_value = mock_user

    user = authenticate_user(db_mock, "test@example.com", "password123")
    assert user is not None
    assert user.email == "test@example.com"


@patch('app.services.auth_service.verify_password')
def test_authenticate_user_not_found(mock_verify_password):
    db_mock = MagicMock(spec=Session)

    # Mock query to return None (user not found)
    db_mock.query.return_value.filter.return_value.first.return_value = None

    user = authenticate_user(db_mock, "nonexistent@example.com", "password123")

    assert user is None
    # Ensure verify_password is called even when user is not found to prevent timing attack
    mock_verify_password.assert_called_once_with("password123", DUMMY_HASH)


def test_authenticate_user_wrong_password():
    db_mock = MagicMock(spec=Session)
    mock_user = MagicMock(spec=User)
    mock_user.email = "test@example.com"
    mock_user.password_hash = hash_password("password123")

    # Mock query to return our mock user
    db_mock.query.return_value.filter.return_value.first.return_value = mock_user

    user = authenticate_user(db_mock, "test@example.com", "wrongpassword")
    assert user is None
