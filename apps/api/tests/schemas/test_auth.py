from app.schemas.auth import SignupRequest
from pydantic import ValidationError
import pytest

def test_signup_request_valid_password():
    req = SignupRequest(email="test@test.com", password="ValidPass123", creator_type="new")
    assert req.password == "ValidPass123"

def test_signup_request_invalid_password_length():
    with pytest.raises(ValidationError) as exc:
        SignupRequest(email="test@test.com", password="short", creator_type="new")
    assert "Password must be at least 8 characters long" in str(exc.value)

def test_signup_request_invalid_password_no_digit():
    with pytest.raises(ValidationError) as exc:
        SignupRequest(email="test@test.com", password="NoDigitsHere", creator_type="new")
    assert "Password must contain at least one digit" in str(exc.value)

def test_signup_request_invalid_password_no_upper():
    with pytest.raises(ValidationError) as exc:
        SignupRequest(email="test@test.com", password="nouppercase123", creator_type="new")
    assert "Password must contain at least one uppercase letter" in str(exc.value)
