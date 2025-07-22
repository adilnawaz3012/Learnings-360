# app/api/v1/endpoints/presentations.py
from fastapi import APIRouter, HTTPException, status, Request
from fastapi.responses import FileResponse
from app.api.v1.schemas.presentation_schemas import (
    PresentationCreateRequest,
    PresentationCreateResponse,
    PresentationStatusResponse,
)
from app.services.presentation_service import presentation_service
from app.services.storage_service import storage_service
from app.core.custom_exceptions import PresentationNotFoundException
from app.core.config import logger

router = APIRouter()

@router.post(
    "/",
    response_model=PresentationCreateResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create a new presentation"
)
async def create_presentation(request: PresentationCreateRequest, http_request: Request):
    """
    Kicks off the presentation generation process.
    
    This endpoint accepts a topic and configuration, creates a presentation record,
    and starts the content and file generation. It immediately returns a response
    with a link to check the status.
    """
    logger.info(f"Received request to create presentation on topic: {request.topic}")
    presentation = await presentation_service.create_new_presentation(request)
    
    status_url = http_request.url_for("get_presentation_details", id=presentation.id)
    
    return PresentationCreateResponse(
        message="Presentation generation started.",
        presentation_id=presentation.id,
        status_url=str(status_url),
    )

@router.get(
    "/{id}",
    response_model=PresentationStatusResponse,
    summary="Retrieve presentation details and status"
)
def get_presentation_details(id: str):
    """
    Retrieves the current status and metadata of a presentation,
    including the download link if generation is complete.
    """
    try:
        presentation = storage_service.get_presentation(id)
        return presentation
    except PresentationNotFoundException as e:
        logger.warning(f"Attempted to access non-existent presentation ID: {id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get(
    "/{id}/download",
    response_class=FileResponse,
    summary="Download presentation as PPTX"
)
def download_presentation(id: str):
    """
    Downloads the generated .pptx file. Returns a 404 if the file
    is not ready or the ID is invalid.
    """
    try:
        presentation = storage_service.get_presentation(id)
        if presentation.status != "completed" or not presentation.file_path:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Presentation is not yet available for download. Status: " + presentation.status
            )
        
        # Create a clean filename for the download
        filename = f"{presentation.topic.replace(' ', '_').lower()}.pptx"
        return FileResponse(
            path=presentation.file_path, 
            media_type='application/vnd.openxmlformats-officedocument.presentationml.presentation',
            filename=filename
        )
    except PresentationNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# Stub for future implementation
@router.post("/{id}/configure", summary="Modify presentation configuration (Not Implemented)")
def modify_presentation_configuration(id: str):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Feature not yet implemented.")