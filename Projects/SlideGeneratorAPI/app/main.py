import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .dependencies import get_settings
from .routes import presentations, auth, cache, health
from .core.celery import celery_app
from app.config import settings
from .database import engine
from .models import database_models

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create database tables (in production, use migrations)
if settings.create_tables:
    logger.info("Creating database tables")
    database_models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url,
    openapi_url=settings.openapi_url
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(presentations.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(cache.router, prefix="/api/v1/cache")
app.include_router(health.router)

# Middleware for request timing
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    from time import perf_counter
    start_time = perf_counter()
    response = await call_next(request)
    process_time = perf_counter() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}"
    return response

# Startup event
@app.on_event("startup")
async def startup_event():
    from .utils.cache import init_cache
    from .core.rate_limiter import init_rate_limiter
    from .services.llm_service import warmup_cache
    
    await init_cache()
    await init_rate_limiter()
    
    # Warm up cache in background
    if settings.warmup_cache:
        await warmup_cache()

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    from .utils.cache import close_cache
    from .services.llm_service import close_http_client
    
    await close_cache()
    await close_http_client()