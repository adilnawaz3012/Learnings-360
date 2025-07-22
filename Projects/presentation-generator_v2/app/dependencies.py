from app.repositories.presentation import PresentationRepository
from app.services.presentation import PresentationService

def get_presentation_repository() -> PresentationRepository:
    return PresentationRepository()

def get_presentation_service(repo: PresentationRepository = Depends()) -> PresentationService:
    return PresentationService(repo)