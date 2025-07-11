from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application settings."""
    OPENAI_API_KEY: str
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://compass.app"
    ]
    MAX_TOKENS: int = 350
    DISCLAIMER: str = "This does not replace professional care."
    
    class Config:
        env_file = ".env"

settings = Settings() 