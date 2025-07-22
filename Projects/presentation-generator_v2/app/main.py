import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api import presentations, auth
from app.core.logging import setup_logging
from app.core.exceptions import PresentationException
from app.core.rate_limiter import limiter
from slowapi.errors import RateLimitExceeded
from app.utils.redis import cache
from contextlib import asynccontextmanager

setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting")
    try:
        cache.get("test_connection")
        logger.info("Cache connection verified")
    except Exception as e:
        logger.error(f"Cache connection failed: {str(e)}")
    yield
    logger.info("Application shutting down")

app = FastAPI(
    title="Presentation Generator API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter

@app.exception_handler(PresentationException)
async def presentation_exception_handler(request: Request, exc: PresentationException):
    return JSONResponse(
        status_code=400,
        content={"message": exc.message, "code": exc.code},
    )

@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests"},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

app.include_router(
    presentations.router,
    prefix="/api/v1/presentations",
    tags=["presentations"]
)

app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["auth"]
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "cache": "active" if cache.client else "inactive"}