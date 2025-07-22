from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # ... (same as app/config.py)
    pass
    
settings = Settings()

def get_settings():
    return settings