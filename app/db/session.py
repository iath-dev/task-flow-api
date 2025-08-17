from sqlalchemy import create_engine
from functools import lru_cache

from app.core.config import settings

@lru_cache()
def get_engine():
    DATABASE_URL = settings.DATABASE_URL
    if DATABASE_URL.startswith("sqlite"):
        return create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    return create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        connect_args={"options": "-c timezone=utc"},
    )