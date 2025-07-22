from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.api.v1.endpoints import router as v1_router
from app.utils.logger import setup_logger
from app.utils.auth import verify_token

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Slide Generator API", version="1.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
setup_logger()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router, prefix="/api/v1", dependencies=[Depends(verify_token)])

@app.get("/")
@limiter.limit("10/minute")
async def root():
    return {"message": "Slide Generator API is up and running"}