# app/api/v1/schemas/presentation_schemas.py
from pydantic import BaseModel
from typing import Optional, List
from app.models.presentation_models import PresentationConfig, Presentation

# Request body for creating a presentation
class PresentationCreateRequest(BaseModel):
    topic: str
    num_slides: int = 5
    custom_content: Optional[List[dict]] = None # For user-provided slide content

# Response model for successful creation
class PresentationCreateResponse(BaseModel):
    message: str
    presentation_id: str
    status_url: str

# Response model for retrieving presentation details
class PresentationStatusResponse(Presentation):
    pass