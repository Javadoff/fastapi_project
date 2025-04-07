from typing import Optional
from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:123456@localhost:5432/postgres"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-here"  # Change this in production!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Project"
    
    class Config:
        case_sensitive = True


settings = Settings()