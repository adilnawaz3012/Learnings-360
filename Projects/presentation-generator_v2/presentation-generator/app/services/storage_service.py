# app/services/storage_service.py
from typing import Dict, Optional
from app.models.presentation_models import Presentation
from app.core.custom_exceptions import PresentationNotFoundException

# In-memory database (dictionary)
_presentations: Dict[str, Presentation] = {}

class StorageService:
    def save_presentation(self, presentation: Presentation):
        """Saves or updates a presentation object."""
        _presentations[presentation.id] = presentation

    def get_presentation(self, presentation_id: str) -> Optional[Presentation]:
        """Retrieves a presentation by its ID."""
        presentation = _presentations.get(presentation_id)
        if not presentation:
            raise PresentationNotFoundException(f"Presentation with ID '{presentation_id}' not found.")
        return presentation

storage_service = StorageService()