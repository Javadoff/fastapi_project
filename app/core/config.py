from typing import Optional
from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:123456@localhost:5432/postgres"
    
    SECRET_KEY: str = "sdfkjndslfksdflkdfj"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    API_STR: str = "/api"
    PROJECT_NAME: str = "FastAPI Project"
    
    class Config:
        case_sensitive = True


settings = Settings()