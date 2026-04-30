from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    VERSION: str = "0.1.0"
    PROJECT_NAME: str = "AlphaConsole"
    
    # Database (Supabase)
    DATABASE_URL: str
    
    # NATS
    NATS_URL: str = "nats://localhost:4222"
    
    # Vector DB & Object Storage
    QDRANT_URL: str = "http://localhost:6333"
    MINIO_ENDPOINT: str = "localhost:9000"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    
    # Security
    SECRET_KEY: str = "super-secret-key-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Vast.ai
    VAST_API_KEY: str
    
    class Config:
        env_file = ".env"

settings = Settings()
