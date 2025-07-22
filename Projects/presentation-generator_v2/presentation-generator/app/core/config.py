# app/core/config.py
import logging
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Presentation Generator API"
    API_V1_STR: str = "/api/v1"
    
    # Placeholder for future service keys
    OPENAI_API_KEY: str = "your_openai_api_key_here"
    PEXELS_API_KEY: str = "your_pexels_api_key_here"

    class Config:
        env_file = ".env"

settings = Settings()

# Basic Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)