from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "TobaGuide Backend API"
    API_V1_STR: str = "/api/v1"
    
    # Database configuration (PostgreSQL)
    # Defaulting to a local PostgreSQL database for development
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/tobaguide"

    # Security configuration
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # RAG & Vector Database Settings
    PINECONE_API_KEY: Optional[str] = None
    PINECONE_INDEX_NAME: str = "tobaguide-index"
    OPENAI_API_KEY: Optional[str] = None
    COHERE_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
