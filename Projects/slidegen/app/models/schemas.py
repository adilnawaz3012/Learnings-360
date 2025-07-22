from pydantic import BaseModel, Field, constr
from typing import Optional

class PresentationRequest(BaseModel):
    topic: constr(min_length=3, max_length=100)
    slide_count: int = Field(5, ge=1, le=20)
    custom_content: Optional[str] = None
    aspect_ratio: Optional[str] = Field(default="16:9", pattern=r"^(4:3|16:9)$")

class PresentationResponse(BaseModel):
    id: str
    message: str

class ConfigureRequest(BaseModel):
    font: Optional[str] = "Arial"
    color: Optional[str] = "000000"