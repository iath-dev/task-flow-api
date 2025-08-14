from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    API_PREFIX: str = '/api/v1'
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRES_MINUTES: int = 60
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000", "http://localhost"]

    class Config:
        env_file = '.env'

settings = Settings()