from typing import Dict, Optional
from uuid import UUID
from app.models.presentation import Presentation
from app.core.logging import logger

class PresentationRepository:
    def __init__(self):
        self.presentations: Dict[UUID, Presentation] = {}

    def save(self, presentation: Presentation):
        self.presentations[presentation.id] = presentation
        logger.info(f"Saved presentation: {presentation.id}")

    def get(self, id: UUID) -> Optional[Presentation]:
        return self.presentations.get(id)
    
    def delete(self, id: UUID):
        if id in self.presentations:
            del self.presentations[id]
            return True
        return False