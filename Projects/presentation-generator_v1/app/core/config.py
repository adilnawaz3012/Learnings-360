from pydantic_settings import BaseSettings
from pydantic import Field
import os

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4-turbo"
    # OPENAI_API_KEY: str = Field(default=os.getenv("OPENAI_API_KEY", ""))
    SECRET_KEY: str = Field(default=os.getenv("SECRET_KEY", "secret-key"))
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    TEMPLATE_DIR: str = Field(default="templates")
    STORAGE_PATH: str = Field(default="storage")
    LOG_LEVEL: str = Field(default="INFO")
    REDIS_URL: str = Field(default=os.getenv("REDIS_URL", "redis://redis:6379"))
    RATE_LIMIT_PER_MINUTE: int = 100

    cache_ttl: int = 3600
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "allow"

settings = Settings()