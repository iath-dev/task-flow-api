from pydantic import EmailStr
from typing import Optional
from app.schemas.common import IdSchema


class UserBase(IdSchema):
    email: EmailStr
    full_name: Optional[str]

    class Config:
        from_attributes = True
