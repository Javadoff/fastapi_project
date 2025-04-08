from typing import Optional
from pydantic.v1 import BaseSettings
import os


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:123456@localhost:5432/postgres")
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "sdfkjndslfksdflkdfj")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
    
    BACKEND_CORS_ORIGINS: list[str] = os.getenv("BACKEND_CORS_ORIGINS", ["http://localhost:3000", "http://localhost:8000"])
    
    API_STR: str = "/api"
    PROJECT_NAME: str = "FastAPI Project"
    
    class Config:
        case_sensitive = True


settings = Settings()