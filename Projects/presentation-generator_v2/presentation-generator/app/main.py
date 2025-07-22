# app/main.py
import os
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.api.v1.endpoints import presentations
from app.core.config import settings, logger
from app.core.custom_exceptions import PresentationNotFoundException

# Create the output directory if it doesn't exist
os.makedirs("generated_presentations", exist_ok=True)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="A backend service to generate customizable presentations.",
)

# --- Exception Handlers ---
@app.exception_handler(PresentationNotFoundException)
async def presentation_not_found_handler(request: Request, exc: PresentationNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error for request {request.method} {request.url}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Invalid request body", "errors": exc.errors()},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.critical(f"Unhandled exception for request {request.method} {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected internal server error occurred."},
    )


# --- API Routers ---
app.include_router(
    presentations.router,
    prefix=settings.API_V1_STR + "/presentations",
    tags=["Presentations"],
)

@app.get("/", tags=["Root"])
def read_root():
    """A simple health check endpoint."""
    return {"status": "ok", "message": f"Welcome to {settings.APP_NAME}"}