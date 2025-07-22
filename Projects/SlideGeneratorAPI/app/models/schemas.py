from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class SlideType(str, Enum):
    TITLE = "title"
    TITLE_AND_CONTENT = "title_and_content"
    SECTION_HEADER = "section_header"
    TWO_COLUMN = "two_column"
    COMPARISON = "comparison"
    IMAGE_WITH_CAPTION = "image_with_caption"

class SlideConfig(BaseModel):
    slide_type: SlideType
    title: str
    content: Optional[str] = None
    image_description: Optional[str] = None
    image_url: Optional[str] = None

class PresentationConfig(BaseModel):
    title: str
    author: Optional[str] = "AI Presentation Generator"
    theme: Optional[str] = "default"
    slides: List[SlideConfig]

class PresentationRequest(BaseModel):
    topic: str
    slide_count: Optional[int] = Field(5, gt=0, le=20)
    include_images: Optional[bool] = False
    custom_instructions: Optional[str] = None
    cache_key: Optional[str] = None

class PresentationResponse(BaseModel):
    id: str
    title: str
    owner_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    config: PresentationConfig
    generation_time: Optional[int] = None

class ConfigurePresentationRequest(BaseModel):
    slide_updates: Optional[List[SlideConfig]] = None
    theme: Optional[str] = None
    author: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserInDB(UserCreate):
    hashed_password: str

class AspectRatio(str, Enum):
    STANDARD = "4:3"
    WIDESCREEN = "16:9"
    CUSTOM = "custom"

class PresentationTemplateRequest(BaseModel):
    template_id: str
    aspect_ratio: Optional[AspectRatio] = AspectRatio.WIDESCREEN
    custom_width: Optional[int] = None
    custom_height: Optional[int] = None

class Template(BaseModel):
    id: str
    name: str
    description: str
    aspect_ratio: AspectRatio
    layout_config: Dict[str, Any]
    preview_image: Optional[str] = None