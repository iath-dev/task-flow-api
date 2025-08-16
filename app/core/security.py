from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.schemas.user import UserBase

# Hasher
pwd_context = CryptContext(schemes=["bcrypt"])

# JWT Config
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRES_MINUTES = settings.ACCESS_TOKEN_EXPIRES_MINUTES
REFRESH_TOKEN_EXPIRES_MINUTES = settings.REFRESH_TOKEN_EXPIRES_MINUTES

# =================
# Password Utils
# =================


def hash_password(password: str) -> str:
    """
    Method to hash the password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Method to verify the password
    """
    return pwd_context.verify(plain_password, hashed_password)


# =================
# JWT Utils
# =================


def create_access_token(
    user: UserBase, expires_delta: Optional[timedelta] = None
) -> str:
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    )
    to_encode = {"sub": str(user), "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str, options: Optional[dict] = None) -> Optional[dict]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options=options)
    except JWTError:
        return None


def get_token_data(token: str, ignore_expiration: bool = False) -> dict:
    options = {"verify_exp": not ignore_expiration}
    payload = decode_token(token, options=options)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload
