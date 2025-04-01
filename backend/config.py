# backend/config.py
import os
from pathlib import Path
from pydantic import BaseSettings, PostgresDsn, validator, Field
from typing import List, Dict, Any, Optional
import secrets

class Settings(BaseSettings):
    # Application Config
    PROJECT_NAME: str = "MarkAI"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Server Config
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    
    # Database Config
    DB_HOST: str = "db"
    DB_PORT: str = "5432"
    DB_USER: str = "markai_user"
    DB_PASSWORD: str = secrets.token_urlsafe(32)
    DB_NAME: str = "markai_db"
    DATABASE_URL: Optional[PostgresDsn] = None
    
    # JWT Config
    JWT_SECRET: str = secrets.token_hex(32)
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000"
    ]
    
    # AI Models
    AI_MODELS_DIR: Path = Path("/app/ai_models")
    
    # File Handling
    UPLOAD_DIR: Path = Path("/app/uploads")
    PROCESSED_DIR: Path = Path("/app/processed")
    MAX_FILE_SIZE: int = 100  # MB
    
    # Model Validation
    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("DB_USER"),
            password=values.get("DB_PASSWORD"),
            host=values.get("DB_HOST"),
            port=values.get("DB_PORT"),
            path=f"/{values.get('DB_NAME')}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()