from enum import Enum
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime
from app.core.config import settings

class SlideLayout(str, Enum):
    TITLE = "title"
    BULLET_POINTS = "bullet_points"
    TWO_COLUMN = "two_column"
    IMAGE_PLACEHOLDER = "image_placeholder"

class AspectRatio(str, Enum):
    SIXTEEN_NINE = "16:9"
    FOUR_THREE = "4:3"
    WIDE = "wide"
    STANDARD = "standard"

class ThemeConfig(BaseModel):
    name: str = "default"
    primary_color: str = "#2A5CAA"
    secondary_color: str = "#FFFFFF"
    accent_color: str = "#FF6B00"
    font: str = "Calibri"
    title_font_size: int = 44
    content_font_size: int = 28
    aspect_ratio: AspectRatio = Field(default=AspectRatio.SIXTEEN_NINE)
    template: Optional[str] = None

    @validator('primary_color', 'secondary_color', 'accent_color')
    def validate_hex_color(cls, v):
        if not v.startswith('#') or len(v) != 7:
            raise ValueError("Color must be in HEX format (#RRGGBB)")
        return v

class SlideContent(BaseModel):
    title: str
    bullets: Optional[List[str]] = None
    columns: Optional[Dict[str, str]] = None
    image_suggestion: Optional[str] = None
    citations: Optional[List[str]] = None

class SlideConfig(BaseModel):
    layout: SlideLayout
    content: SlideContent

class PresentationCreate(BaseModel):
    topic: str
    custom_content: Optional[str] = None
    num_slides: int = Field(5, ge=1, le=20)
    theme: ThemeConfig = Field(default_factory=ThemeConfig)

class PresentationUpdate(BaseModel):
    theme: Optional[ThemeConfig] = None
    slides: Optional[List[SlideConfig]] = None

class Presentation(PresentationCreate):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    slides: List[SlideConfig] = []
    pptx_path: Optional[str] = None
    owner: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str