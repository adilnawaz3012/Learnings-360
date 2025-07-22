from celery import shared_task
from app.core.celery import celery_app
from app.services import llm_service, image_service, pptx_generator
from app.models.schemas import PresentationConfig
from app.database import SessionLocal
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, acks_late=True, time_limit=300)
def generate_pptx_task(self, presentation_id: str, config_dict: dict, user_id: int,
                      template_id: str = "modern", aspect_ratio: str = "16:9",
                      custom_size: tuple = None):
    db = SessionLocal()
    
    try:
        start_time = datetime.now()
        config = PresentationConfig(**config_dict)
        
        # Generate images in parallel
        generate_images_for_slides(config)
        
        # Generate PPTX
        pptx_buffer = pptx_generator.create_pptx(
            config, template_id, aspect_ratio, custom_size
        )
        
        # Save to file
        os.makedirs("storage/presentations", exist_ok=True)
        pptx_path = f"storage/presentations/{presentation_id}.pptx"
        with open(pptx_path, "wb") as f:
            f.write(pptx_buffer.getvalue())
        
        # Update database
        presentation = db.query(PresentationDB).filter_by(id=presentation_id).first()
        if presentation:
            presentation.pptx_path = pptx_path
            presentation.status = "completed"
            presentation.generation_time = (datetime.now() - start_time).total_seconds() * 1000
            db.commit()
        
        return {"status": "completed", "presentation_id": presentation_id}
    
    except Exception as e:
        logger.error(f"Error in generate_pptx_task: {str(e)}")
        presentation = db.query(PresentationDB).filter_by(id=presentation_id).first()
        if presentation:
            presentation.status = "failed"
            db.commit()
        raise self.retry(exc=e, countdown=60, max_retries=3)
    finally:
        db.close()

def generate_images_for_slides(config: PresentationConfig):
    from concurrent.futures import ThreadPoolExecutor
    
    slides_needing_images = [
        slide for slide in config.slides 
        if slide.image_description and not slide.image_url
    ]
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for slide in slides_needing_images:
            futures.append(executor.submit(
                generate_image_sync, 
                slide.image_description
            ))
        
        for future, slide in zip(futures, slides_needing_images):
            image_url = future.result()
            if image_url:
                slide.image_url = image_url

def generate_image_sync(prompt: str):
    # Synchronous wrapper for image generation
    import asyncio
    from app.services.image_service import generate_image
    return asyncio.run(generate_image(prompt))