import uuid
import os
import logging
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from fastapi.responses import FileResponse
from app.services.content import ContentService
from app.services.presentation import PresentationService, PPTXGenerationException
from app.models.presentation import Presentation, PresentationCreate, PresentationUpdate
from app.repositories.presentation import PresentationRepository
from app.core.security import get_current_user
from app.core.rate_limiter import limiter
from app.core.config import settings
from app.services.storage import save_template
from app.utils.redis import cache
from app.models.presentation import Presentation, PresentationCreate, PresentationUpdate, TokenData, PresentationResponse
from openai import AsyncOpenAI, APIStatusError, APITimeoutError, APIConnectionError


router = APIRouter()
logger = logging.getLogger(__name__)

@router.post(
    "/", 
    response_model=PresentationResponse, 
    status_code=status.HTTP_201_CREATED
)
async def create_presentation(
    request: PresentationCreate,
    content_svc: ContentService = Depends(),
    repo: PresentationRepository = Depends(),
    username: str = Depends(get_current_user)
):
    try:
        # Validate theme template exists if provided
        if request.theme.template:
            template_path = os.path.join(settings.TEMPLATE_DIR, request.theme.template)
            if not os.path.exists(template_path):
                raise HTTPException(
                    status_code=400, 
                    detail=f"Template '{request.theme.template}' not found"
                )
        
        # Generate content FIRST using the service
        slides_content = await content_svc.generate_content(
            topic=request.topic,
            num_slides=request.num_slides,
            theme=request.theme
        )
        
        # Create presentation with generated content
        presentation = Presentation(
            **request.dict(),
            slides=slides_content,  # Add generated content here
            owner=username
        )
        
        # Save to repository
        repo.save(presentation)
        return presentation
        
    except Exception as e:
        logger.exception(f"Presentation creation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 

@router.get("/{id}", response_model=Presentation)
async def get_presentation(
    id: uuid.UUID, 
    repo: PresentationRepository = Depends(),
    current_user: str = Depends(get_current_user)
):
    if presentation := repo.get(id):
        if presentation.owner != current_user.username:
            raise HTTPException(403, detail="Unauthorized access")
        return presentation
    raise HTTPException(404, detail="Presentation not found")

@router.post("/{id}/configure", response_model=Presentation)
async def configure_presentation(
    id: uuid.UUID, 
    config: PresentationUpdate,
    repo: PresentationRepository = Depends(),
    current_user: str = Depends(get_current_user)
):
    if presentation := repo.get(id):
        if presentation.owner != current_user.username:
            raise HTTPException(403, detail="Unauthorized access")
        
        updated_data = presentation.dict()
        if config.theme:
            updated_data['theme'] = {**presentation.theme.dict(), **config.theme.dict(exclude_unset=True)}
        if config.slides:
            updated_data['slides'] = config.slides
        
        updated_presentation = Presentation(**updated_data)
        repo.save(updated_presentation)
        cache.delete(f"pptx:{id}")
        return updated_presentation
        
    raise HTTPException(404, detail="Presentation not found")

@router.get("/{id}/download")
async def download_presentation(
    id: uuid.UUID, 
    presentation_svc: PresentationService = Depends(),
    repo: PresentationRepository = Depends(),
    current_user: str = Depends(get_current_user)
):
    if not (presentation := repo.get(id)):
        raise HTTPException(404, detail="Presentation not found")
    
    if presentation.owner != current_user.username:
        raise HTTPException(403, detail="Unauthorized access")
    
    try:
        pptx_path = await presentation_svc.generate_pptx(presentation)
        return FileResponse(
            pptx_path,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            filename=f"{presentation.topic}.pptx"
        )
    except PPTXGenerationException as e:
        raise HTTPException(503, detail=str(e))

@router.post("/templates/upload")
async def upload_template(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user)
):
    if not file.filename.endswith('.pptx'):
        raise HTTPException(400, detail="Only PPTX files are allowed")
    
    try:
        file_path = save_template(file)
        return {"filename": file.filename, "path": file_path}
    except Exception as e:
        raise HTTPException(500, detail="Failed to save template")
    
@router.get("/health")
async def health_check():
    try:
        # Check if API key is configured
        if not settings.OPENAI_API_KEY:
            return {"status": "ERROR", "detail": "OpenAI API key not configured"}
        
        # Perform lightweight check
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        await client.with_options(max_retries=0).models.retrieve("gpt-3.5-turbo")
        return {"status": "OK"}
    
    except (APIStatusError, APITimeoutError, APIConnectionError) as e:
        return {"status": "ERROR", "detail": f"OpenAI connection failed: {e.message}"}
    
    except Exception as e:
        return {"status": "ERROR", "detail": f"Unexpected error: {str(e)}"}