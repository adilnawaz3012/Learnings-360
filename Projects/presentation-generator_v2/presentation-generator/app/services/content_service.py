# app/services/content_service.py
import random
from app.models.presentation_models import PresentationData, Slide, SlideLayout
from app.core.custom_exceptions import ContentGenerationException
from app.core.config import logger

class ContentService:
    async def generate_content_from_topic(self, topic: str, num_slides: int) -> PresentationData:
        """
        Simulates generating presentation content from a topic using an LLM.
        In a real application, this would call OpenAI, Gemini, etc.
        """
        logger.info(f"Generating mock content for topic: {topic}")
        try:
            # Mock LLM behavior
            slides = [Slide(type=SlideLayout.TITLE, title=topic, subtitle=f"A Deep Dive by AI")]
            
            for i in range(num_slides - 2): # -2 for title and citation slides
                layout = random.choice([
                    SlideLayout.BULLET_POINTS, 
                    SlideLayout.TWO_COLUMN, 
                    SlideLayout.CONTENT_WITH_IMAGE
                ])
                if layout == SlideLayout.BULLET_POINTS:
                    slides.append(Slide(type=layout, title=f"Key Point {i+1}", points=[f"Detail A for point {i+1}", f"Detail B for point {i+1}", f"Detail C for point {i+1}"]))
                elif layout == SlideLayout.TWO_COLUMN:
                     slides.append(Slide(type=layout, title=f"Comparison {i+1}", left_content="Column 1 text about the topic.", right_content="Column 2 text providing more details."))
                else: # CONTENT_WITH_IMAGE
                    slides.append(Slide(type=layout, title=f"Visual Concept {i+1}", content="This slide illustrates a key concept with an image.", image_suggestion=f"{topic} concept art"))

            # Add a final citation slide
            slides.append(Slide(type=SlideLayout.BULLET_POINTS, title="Sources & Citations", points=["Source: AI Content Generator Mock Service, 2025", "Images: Suggested by AI, sourced from placeholder APIs."]))

            return PresentationData(title=topic, slides=slides, citations=["Mock Citation 1", "Mock Citation 2"])
        
        except Exception as e:
            logger.error(f"Failed to generate content: {e}")
            raise ContentGenerationException(f"Error in mock content generation for topic '{topic}'.")

content_service = ContentService()