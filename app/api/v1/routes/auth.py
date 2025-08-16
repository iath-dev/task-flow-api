from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.auth import RegisterResponse, RegisterRequest
from app.services import auth_service

router = APIRouter(prefix="/auth")


@router.post("/login", tags=["Auth"])
def authenticate():
    return True


@router.post(
    "/signin",
    tags=["Auth"],
    status_code=status.HTTP_202_ACCEPTED,
    description="Register user",
    response_model=RegisterResponse,
)
def register(register_data: RegisterRequest, db: Session = Depends(get_db)):
    return auth_service.register(db, register_data=register_data)
