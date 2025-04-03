from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """Settings for the application"""
    DATABASE_URL: str = "sqlite+aiosqlite://test.db"  # fallback for tests
    API_PREFIX: str = "/api"
    ALGORITHM:str  = "ES512"
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 30
    PROD: bool = False
    
    model_config = ConfigDict(env_file=".env",)


settings = Settings()
