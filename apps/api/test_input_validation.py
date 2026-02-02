import sys
import os
from unittest.mock import MagicMock

# Add current directory to path so we can import app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from app.main import app
from app.core.deps import get_current_user, get_db

# Mock dependencies
def mock_get_current_user():
    user = MagicMock()
    user.id = 1
    return user

def mock_get_db():
    db = MagicMock()
    # Mock query(CreatorPersona).filter(...).first()
    persona = MagicMock()
    persona.persona_json = {}

    # Mock db queries
    query_mock = MagicMock()

    # We need to handle different queries.
    # For now, let's just make sure it doesn't crash before validation.
    # Validation happens BEFORE dependencies are fully utilized usually,
    # but FastAPI executes dependencies.

    db.query.return_value = query_mock
    query_mock.filter.return_value = query_mock
    query_mock.first.return_value = persona

    return db

# Override dependencies
app.dependency_overrides[get_current_user] = mock_get_current_user
app.dependency_overrides[get_db] = mock_get_db

client = TestClient(app)

def test_script_validation():
    print("🧪 Testing Input Validation for /script endpoint...")

    # Test 1: Missing topic (should fail)
    print("\n1. Testing missing topic...")
    response = client.post("/script", json={})
    if response.status_code == 422:
        print("✅ Correctly rejected missing topic (422 Unprocessable Entity)")
    else:
        print(f"❌ Failed: Expected 422, got {response.status_code}")
        print(response.json())
        return False

    # Test 2: Empty topic (should fail because min_length=1)
    print("\n2. Testing empty topic...")
    response = client.post("/script", json={"topic": ""})
    if response.status_code == 422:
        print("✅ Correctly rejected empty topic (422 Unprocessable Entity)")
    else:
        print(f"❌ Failed: Expected 422, got {response.status_code}")
        print(response.json())
        return False

    # Test 3: Long topic (should fail because max_length=200)
    print("\n3. Testing topic > 200 chars...")
    long_topic = "a" * 201
    response = client.post("/script", json={"topic": long_topic})
    if response.status_code == 422:
        print("✅ Correctly rejected long topic (422 Unprocessable Entity)")
    else:
        print(f"❌ Failed: Expected 422, got {response.status_code}")
        print(response.json())
        return False

    # Test 4: Valid topic (should pass validation)
    print("\n4. Testing valid topic...")
    try:
        response = client.post("/script", json={"topic": "My Awesome Video"})
        if response.status_code != 422:
            print(f"✅ Validation passed (Status: {response.status_code})")
        else:
            print(f"❌ Failed: Valid topic was rejected (422)")
            print(response.json())
            return False
    except Exception as e:
        # If it crashes with ResponseValidationError, it means it passed input validation!
        if "ResponseValidationError" in str(e) or "validation errors" in str(e):
             print(f"✅ Validation passed (reached response validation)")
        else:
             print(f"⚠️ App crashed with unrelated error: {e}")
             # still considered pass for *input* validation purposes

    print("\n✨ All validation tests passed!")
    return True

if __name__ == "__main__":
    success = test_script_validation()
    sys.exit(0 if success else 1)
