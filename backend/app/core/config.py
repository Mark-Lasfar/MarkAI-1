from pydantic import BaseSettings, Field, PostgresDsn, validator
from typing import List, Dict, Any
import os
from pathlib import Path
import secrets

class Settings(BaseSettings):
    # Application Configuration
    PROJECT_NAME: str = Field(default="MarkAI", env="PROJECT_NAME")
    VERSION: str = Field(default="1.0.0", env="VERSION")
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # Server Configuration
    SERVER_HOST: str = Field(default="0.0.0.0", env="SERVER_HOST")
    SERVER_PORT: int = Field(default=8000, env="SERVER_PORT")
    
    # Database Configuration
    DB_HOST: str = Field(default="localhost", env="DB_HOST")
    DB_PORT: str = Field(default="5432", env="DB_PORT")
    DB_USER: str = Field(default="markai_user", env="DB_USER")
    DB_PASSWORD: str = Field(default=secrets.token_urlsafe(32), env="DB_PASSWORD")
    DB_NAME: str = Field(default="markai_db", env="DB_NAME")
    DATABASE_URL: PostgresDsn = None
    
    # JWT Configuration
    JWT_SECRET: str = Field(default=secrets.token_hex(32), env="JWT_SECRET")
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    JWT_EXPIRE_MINUTES: int = Field(default=60, env="JWT_EXPIRE_MINUTES")
    
    # Security Configuration
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost", "http://localhost:3000"],
        env="ALLOWED_ORIGINS"
    )
    
    # AI Configuration
    AI_MODELS_DIR: Path = Field(
        default=Path(__file__).resolve().parent.parent / "ai_models",
        env="AI_MODELS_DIR"
    )
    
    # File Storage Configuration
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    UPLOAD_FOLDER: Path = Field(default=BASE_DIR / "uploads")
    PROCESSED_FOLDER: Path = Field(default=BASE_DIR / "processed")
    MAX_FILE_SIZE_MB: int = Field(default=100, env="MAX_FILE_SIZE_MB")
    
    # File Type Restrictions
    ALLOWED_FILE_TYPES: Dict[str, List[str]] = Field(
        default={
            'image': ['jpg', 'jpeg', 'png', 'webp'],
            'document': ['pdf', 'docx', 'txt'],
            'archive': ['zip', 'rar'],
            'media': ['mp3', 'mp4', 'avi', 'mov']
        }
    )
    
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
    
    @validator("ALLOWED_ORIGINS", pre=True)
    def parse_allowed_origins(cls, v: str) -> List[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    # Initialization
    def init_app(self, app):
        """Initialize application directories and settings"""
        self.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
        self.PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)
        self.AI_MODELS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Security middleware configuration
        if not self.DEBUG:
            app.add_middleware(
                HTTPSRedirectMiddleware,
                https_port=self.SERVER_PORT
            )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        secrets_dir = "/run/secrets"  # For Docker secrets

# Initialize settings
settings = Settings()