import sys
import os

# Add apps/api to sys.path so we can import app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import MagicMock
from app.services.auth_service import authenticate_user

def test_authenticate_user_invalid_user_timing_mitigation(mocker):
    # Mock the database session
    db = MagicMock()
    # Mock the query result to return None (user not found)
    db.query.return_value.filter.return_value.first.return_value = None

    # Mock verify_password
    mock_verify = mocker.patch("app.services.auth_service.verify_password")

    # Call authenticate_user with a non-existent user
    result = authenticate_user(db, "nonexistent@example.com", "somepassword")

    # Assert that result is None
    assert result is None

    # Assert that verify_password was called to mitigate timing attacks
    assert mock_verify.called, "verify_password should be called even for non-existent users to prevent timing attacks"
