import sys
import os
import unittest
from unittest.mock import MagicMock
from app.services.auth_service import authenticate_user
from app.core.security import hash_password

class TestAuthSecurity(unittest.TestCase):
    def test_authenticate_user_not_found(self):
        """
        Verify that authenticate_user returns None when user is not found,
        and (implicitly via code inspection/timing tests) performs a dummy hash check.
        """
        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = None

        user = authenticate_user(mock_db, "nonexistent@example.com", "password123")
        self.assertIsNone(user)

    def test_authenticate_user_wrong_password(self):
        """
        Verify that authenticate_user returns None when password is correct but hash mismatch.
        """
        mock_db = MagicMock()
        mock_user = MagicMock()
        mock_user.password_hash = hash_password("correct_password")
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user

        user = authenticate_user(mock_db, "exists@example.com", "wrong_password")
        self.assertIsNone(user)

    def test_authenticate_user_success(self):
        """
        Verify that authenticate_user returns user when password is correct.
        """
        mock_db = MagicMock()
        mock_user = MagicMock()
        password = "correct_password"
        mock_user.password_hash = hash_password(password)
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user

        user = authenticate_user(mock_db, "exists@example.com", password)
        self.assertEqual(user, mock_user)

if __name__ == "__main__":
    unittest.main()
