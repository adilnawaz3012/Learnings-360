import json
import logging
from datetime import datetime
from ..utils.cache import get_cache, set_cache
from ..core.config import get_settings
from ..models.schemas import PresentationConfig, SlideConfig
from ..utils.http_client import get_async_client

logger = logging.getLogger(__name__)
settings = get_settings()
async_client = get_async_client()

async def generate_with_llm(prompt: str, max_tokens: int = 1000) -> str:
    cache_key = f"llm:{hash(prompt)}"
    
    # Check cache
    if cached := await get_cache(cache_key):
        return cached
    
    try:
        # Use optimized prompt structure
        optimized_prompt = f"""
        [SYSTEM]
        You are an expert presentation content generator. 
        Respond with concise, structured content suitable for slides.
        Use bullet points when appropriate.
        Avoid lengthy paragraphs.
        
        [TASK]
        {prompt}
        """
        
        response = await async_client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.openai_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": optimized_prompt}],
                "max_tokens": max_tokens,
                "temperature": 0.7,
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"OpenAI API error: {response.text}")
        
        data = response.json()
        content = data['choices'][0]['message']['content'].strip()
        
        # Cache results
        await set_cache(cache_key, content, 3600)  # 1 hour
        
        return content
    except Exception as e:
        logger.error(f"Error in LLM generation: {str(e)}")
        raise HTTPException(status_code=500, detail="Content generation failed")

async def generate_presentation_structure(topic: str, slide_count: int, include_images: bool, custom_instructions: str = None) -> PresentationConfig:
    cache_key = f"pres_struct:{topic}:{slide_count}:{include_images}:{custom_instructions}"
    
    # Check cache
    if cached := await get_cache(cache_key):
        try:
            data = json.loads(cached)
            return PresentationConfig(**data)
        except json.JSONDecodeError:
            logger.warning("Cached data corrupted, regenerating...")
    
    # Generate optimized prompt
    prompt = f"""
    Create a presentation outline about {topic} with exactly {slide_count} slides.
    Follow this structure:
    - First slide: Title slide with presentation title
    - Second slide: Table of contents
    - Next {slide_count-4} slides: Main content
    - Last slide: Conclusion and Q&A
    
    For each slide, provide:
    - slide_type: One of title, title_and_content, section_header, two_column, comparison, image_with_caption
    - title: Concise slide title
    - content: 3-5 bullet points max
    - image_description: Only if relevant to content
    
    Guidelines:
    - Keep titles under 10 words
    - Keep content concise
    - Use simple language
    """
    
    if custom_instructions:
        prompt += f"\nAdditional instructions: {custom_instructions}"
    
    if include_images:
        prompt += "\nInclude image suggestions for 30-50% of slides where appropriate."
    
    prompt += "\n\nOutput must be valid JSON only."
    
    start_time = datetime.now()
    response = await generate_with_llm(prompt)
    
    try:
        data = json.loads(response)
        config = PresentationConfig(
            title=data.get("title", f"Presentation about {topic}"),
            slides=[SlideConfig(**slide) for slide in data.get("slides", [])]
        )
        
        # Cache results
        await set_cache(cache_key, json.dumps(config.dict()), 86400)  # 24 hours
        return config
    except json.JSONDecodeError:
        logger.error(f"Failed to parse LLM response as JSON: {response}")
        raise HTTPException(status_code=500, detail="Failed to parse presentation structure")
    except Exception as e:
        logger.error(f"Error generating presentation structure: {str(e)}")
        raise HTTPException(status_code=500, detail="Presentation structure generation failed")

async def warmup_cache():
    # Warm up cache with common requests
    common_topics = ["Climate Change", "Artificial Intelligence", "Renewable Energy"]
    for topic in common_topics:
        cache_key = f"pres_struct:{topic}:5:True:None"
        if not await get_cache(cache_key):
            try:
                await generate_presentation_structure(topic, 5, True)
            except:
                pass

async def close_http_client():
    await async_client.aclose()