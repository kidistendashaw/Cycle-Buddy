from pydantic import BaseModel, EmailStr
from typing import Optional


# ── Base ─────────────────────────
class UserBase(BaseModel):
    full_name: str
    email: EmailStr


# ── Create User (client input) ──
class UserCreate(UserBase):
    password: str


# ── Response (send back to client) ──
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


# ── Login input ──────────────────
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ── JWT Token Response ───────────
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ── Combined response for login/register ──
class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
