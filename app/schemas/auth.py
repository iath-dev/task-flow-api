from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator

from app.schemas.user import UserBase

SPECIALS = "@$!%*?&.#_-"


class TokenData(BaseModel):
    access_token: str
    refresh_token: Optional[str]
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr = Field("user@example.com", description="User register email")
    password: str = Field(
        "bGp*B2t&09OE6h",
        description="User password, 8-30 characters, with uppercase, lowercase, digit, and special character.",
    )

    @field_validator("password")
    def validate_password(cls, v):
        checks = {
            "Must have at lest 1 minus": any(c.islower() for c in v),
            "Must have at lest 1 mayus": any(c.isupper() for c in v),
            "Must have at lest 1 number": any(c.isdigit() for c in v),
            "Must have at lest 1 special char": any(c in SPECIALS for c in v),
        }
        for msg, ok in checks.items():
            if not ok:
                raise ValueError(msg)
        return v


class LoginResponse(TokenData):
    pass


class RegisterRequest(LoginRequest):
    full_name: str


class RegisterResponse(BaseModel):
    message: str = "User registered successfully"
    user: UserBase
    token: Optional[TokenData]
