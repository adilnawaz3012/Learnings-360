from fastapi import Request, HTTPException
from app.core.config import settings

def verify_token(request: Request):
    token = request.headers.get("Authorization")
    if not token or token != f"Bearer {settings.API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")