from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.auth import RegisterRequest, TokenData, RegisterResponse
from app.db.models.user import User
from app.core.security import hash_password, create_access_token


def register(db: Session, register_data: RegisterRequest):
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

    access_token = create_access_token(db_user)
    refresh_token = create_access_token(db_user, expires_delta=timedelta(60 * 24 * 30))

    token = TokenData(access_token=access_token, refresh_token=refresh_token)

    return RegisterResponse(user=db_user, token=token)
