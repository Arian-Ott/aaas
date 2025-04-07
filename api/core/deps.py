from pathlib import Path
from dotenv import load_dotenv
from api.core.config import Settings

# Load .env from two levels up
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path, override=True)

# Now create the settings instance AFTER env is loaded
settings = Settings()