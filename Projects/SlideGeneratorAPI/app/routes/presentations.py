from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_limiter.depends import RateLimiter
from ..services import presentation_service
from ..models.schemas import (
    PresentationRequest,
    PresentationResponse,
    ConfigurePresentationRequest,
    PresentationTemplateRequest
)
from ..dependencies import get_current_active_user, get_rate_limiter

router = APIRouter()

@router.post("/presentations", response_model=PresentationResponse, 
             dependencies=[Depends(RateLimiter(times=5, minutes=1))])
async def create_presentation(
    request: PresentationRequest,
    current_user = Depends(get_current_active_user)
):
    return await presentation_service.create_presentation(request, current_user)

@router.get("/presentations/{presentation_id}", response_model=PresentationResponse)
async def get_presentation(
    presentation_id: str,
    current_user = Depends(get_current_active_user)
):
    return await presentation_service.get_presentation(presentation_id, current_user)

@router.get("/presentations/{presentation_id}/download")
async def download_presentation(
    presentation_id: str,
    current_user = Depends(get_current_active_user)
):
    return await presentation_service.download_presentation(presentation_id, current_user)

@router.post("/presentations/{presentation_id}/configure", response_model=PresentationResponse)
async def configure_presentation(
    presentation_id: str,
    request: ConfigurePresentationRequest,
    current_user = Depends(get_current_active_user)
):
    return await presentation_service.configure_presentation(presentation_id, request, current_user)

@router.post("/presentations/template", response_model=PresentationResponse,
             dependencies=[Depends(get_rate_limiter())])
async def create_presentation_with_template(
    request: PresentationRequest,
    template_request: PresentationTemplateRequest,
    current_user = Depends(get_current_active_user)
):
    return await presentation_service.create_presentation_with_template(
        request, template_request, current_user
    )

@router.post("/presentations/batch", response_model=list[PresentationResponse])
async def create_batch_presentations(
    requests: list[PresentationRequest],
    current_user = Depends(get_current_active_user)
):
    return await presentation_service.create_batch_presentations(requests, current_user)

@router.post("/content/preview", response_model=PresentationResponse)
async def preview_content(
    request: PresentationRequest,
    current_user = Depends(get_current_active_user)
):
    return await presentation_service.preview_content(request)