from typing import Literal
from pydantic import BaseModel, EmailStr, field_validator

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    creator_type: Literal["new", "existing"]

    @field_validator('password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"