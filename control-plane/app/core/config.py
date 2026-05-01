from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional, List

class Settings(BaseSettings):
    VERSION: str = "0.1.0"
    PROJECT_NAME: str = "AlphaConsole"
    
    # Database (Supabase)
    DATABASE_URL: str
    
    # NATS
    NATS_URL: str = "nats://nats:4222"
    
    # Vector DB & Object Storage
    QDRANT_URL: str = "http://qdrant:6333"
    MINIO_ENDPOINT: str = "minio:9000"
    OLLAMA_BASE_URL: str = Field(..., env="OLLAMA_BASE_URL")
    
    # Security
    ALLOWED_ORIGINS: List[str] = ["*"]
    SECRET_KEY: str = "super-secret-key-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Vast.ai
    VAST_API_KEY: str
    
    class Config:
        env_file = ".env"

settings = Settings()
