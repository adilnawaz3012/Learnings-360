import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    API_KEY: str = os.getenv("API_KEY", "test-key")

settings = Settings()