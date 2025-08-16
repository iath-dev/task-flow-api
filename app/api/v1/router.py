from fastapi import APIRouter
from app.api.v1.routes import health, auth

api_router = APIRouter(prefix="/v1")

api_router.include_router(health.router)
api_router.include_router(auth.router)
