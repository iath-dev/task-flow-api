from fastapi import APIRouter, Depends, status, Request

from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.auth import (
    RegisterResponse,
    RegisterRequest,
    LoginRequest,
    LoginResponse,
)
from app.services import auth_service

router = APIRouter(prefix="/auth")


@router.post(
    "/login",
    tags=["Auth"],
    status_code=status.HTTP_200_OK,
    description="Authenticate user with email and password",
    summary="Authenticate user",
    response_model=LoginResponse,
)
def authenticate(
    login_data: LoginRequest, db: Session = Depends(get_db), request: Request = None
):
    token = auth_service.login_user(login_data=login_data, db=db, request=request)
    db.commit()
    return token


@router.post(
    "/register",
    tags=["Auth"],
    status_code=status.HTTP_202_ACCEPTED,
    description="Register an user in the database",
    summary="Register user",
    response_model=RegisterResponse,
)
def register(register_data: RegisterRequest, db: Session = Depends(get_db)):
    return auth_service.register_user(db, register_data=register_data)
