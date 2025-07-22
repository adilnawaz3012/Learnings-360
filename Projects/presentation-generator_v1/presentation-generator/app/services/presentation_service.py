# app/services/presentation_service.py
from app.models.presentation_models import Presentation, PresentationConfig
from app.api.v1.schemas.presentation_schemas import PresentationCreateRequest
from .storage_service import storage_service
from .content_service import content_service
from app.utils.pptx_builder import create_presentation_file
from app.core.config import logger

class PresentationService:
    async def create_new_presentation(self, request: PresentationCreateRequest) -> Presentation:
        """
        Main orchestration logic for creating a new presentation.
        NOTE: This is currently synchronous. For production, this should be
        a background task (e.g., using Celery or FastAPI's BackgroundTasks).
        """
        # 1. Create and save the initial presentation record
        config = PresentationConfig(num_slides=request.num_slides)
        presentation = Presentation(topic=request.topic, config=config)
        storage_service.save_presentation(presentation)
        logger.info(f"Created new presentation record with ID: {presentation.id}")
        
        try:
            # 2. Generate content (mock LLM call)
            # TODO: Handle request.custom_content to override generated content
            presentation.content = await content_service.generate_content_from_topic(
                topic=presentation.topic, 
                num_slides=presentation.config.num_slides
            )
            
            # 3. Generate the .pptx file
            presentation.file_path = create_presentation_file(
                data=presentation.content, 
                config=presentation.config
            )
            
            # 4. Update status to completed
            presentation.status = "completed"
            logger.info(f"Successfully generated presentation {presentation.id}")

        except Exception as e:
            presentation.status = "failed"
            logger.error(f"Presentation {presentation.id} failed: {e}")
        
        finally:
            # 5. Save the final state
            storage_service.save_presentation(presentation)
            return presentation

presentation_service = PresentationService()