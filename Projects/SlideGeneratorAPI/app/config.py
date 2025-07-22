from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Presentation Generation API"
    app_description: str = "API for generating presentations with AI-powered content"
    app_version: str = "1.0.0"
    app_env: str = "development"
    
    docs_url: str = "/api/docs"
    redoc_url: str = "/api/redoc"
    openapi_url: str = "/api/openapi.json"
    
    database_url: str
    redis_url: str
    cache_redis_url: str
    celery_broker_url: str
    celery_result_backend: str
    
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    openai_api_key: str
    
    allowed_origins: list = ["*"]
    create_tables: bool = False
    warmup_cache: bool = True
    rate_limit_per_minute: int = 60
    
    class Config:
        env_file = ".env"

settings = Settings()