from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"  # fallback for tests
    API_PREFIX: str = "/api"

    class Config:
        env_file = ".env"

settings = Settings()