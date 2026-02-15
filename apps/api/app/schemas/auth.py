from typing import Literal
from pydantic import BaseModel, EmailStr, Field, field_validator
import re

class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long")
    creator_type: Literal["new", "existing"]

    @field_validator('password')
    @classmethod
    def validate_password_complexity(cls, v: str) -> str:
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
