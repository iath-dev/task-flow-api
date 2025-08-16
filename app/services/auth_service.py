from datetime import timedelta
from fastapi import HTTPException, status, Request
from sqlalchemy.orm import Session

from app.schemas.auth import RegisterRequest, TokenData, RegisterResponse, LoginRequest
from app.db.models.user import User, UserStatusEnum
from app.core.security import hash_password, create_access_token, verify_password
from app.db.models.logs import LoginLog, LogStatusEnum


def create_login_log(
    db: Session,
    request: Request,
    status: LogStatusEnum,
    user_id: int,
    reason: str | None = None,
):
    db_log = LoginLog(
        user_id=user_id,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        status=status,
        reason=reason,
    )
    db.add(db_log)
    db.commit()


def generate_token(db_user: User) -> TokenData:
    access_token = create_access_token(db_user)
    refresh_token = create_access_token(db_user, expires_delta=timedelta(60 * 24 * 30))

    return TokenData(access_token=access_token, refresh_token=refresh_token)


def login_user(db: Session, login_data: LoginRequest, request: Request):
    db_user = db.query(User).filter(User.email == login_data.email).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    if (
        not verify_password(login_data.password, db_user.password)
        or db_user.status is not UserStatusEnum.active
    ):
        create_login_log(
            db,
            request,
            LogStatusEnum.failed,
            user_id=db_user.id,
            reason="Invalid password or inactive user",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    token = generate_token(db_user)
    create_login_log(db, request, LogStatusEnum.success, user_id=db_user.id)

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
