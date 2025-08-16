from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.auth import RegisterRequest, TokenData, RegisterResponse, LoginRequest
from app.db.models.user import User, StatusEnum
from app.core.security import hash_password, create_access_token, verify_password


def generate_token(db_user: User) -> TokenData:
    access_token = create_access_token(db_user)
    refresh_token = create_access_token(db_user, expires_delta=timedelta(60 * 24 * 30))

    return TokenData(access_token=access_token, refresh_token=refresh_token)


def login_user(db: Session, login_data: LoginRequest):
    db_user = db.query(User).filter(User.email == login_data.email).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    if (
        not verify_password(login_data.password, db_user.password)
        or db_user.status is not StatusEnum.active
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    token = generate_token(db_user)

    return token


def register_user(db: Session, register_data: RegisterRequest):
    check_user = db.query(User).filter(User.email == register_data.email).first()

    if check_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data"
        )

    db_user = User(
        email=register_data.email,
        full_name=register_data.full_name,
        password=hash_password(password=register_data.password),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    token = generate_token(db_user)

    return RegisterResponse(user=db_user, token=token)
