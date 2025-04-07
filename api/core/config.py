from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from pathlib import Path
from ssl import RAND_bytes

class Settings(BaseSettings):
    """Settings for the application"""
    DATABASE_URL: str = "sqlite:///./test.db"
    API_PREFIX: str = "/api"
    ALGORITHM:str  = "ES512"
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 30
    PROD: bool = False
    SECRET_KEY:str = ""
    PROJECT_NAME: str = "Authentication as a Service"
    VERSION: str = "0.1.0"
 
    
    model_config = ConfigDict(env_file=Path(__file__).resolve().parents[2] / ".env", env_file_encoding="utf-8", case_sensitive=False )


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
       
        if self.PROD and self.SECRET_KEY == "":
            raise ValueError("SECRET_KEY must be set in production mode")
        elif not self.PROD and self.SECRET_KEY == "":
            self.SECRET_KEY = RAND_bytes(32).hex()