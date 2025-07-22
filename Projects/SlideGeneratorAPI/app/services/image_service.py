import logging
from ..utils.cache import get_cache, set_cache
from ..core.config import get_settings
from ..utils.http_client import get_async_client

logger = logging.getLogger(__name__)
settings = get_settings()
async_client = get_async_client()

async def generate_image(prompt: str) -> str:
    cache_key = f"image:{hash(prompt)}"
    
    # Check cache
    if cached := await get_cache(cache_key):
        return cached
    
    try:
        response = await async_client.post(
            "https://api.openai.com/v1/images/generations",
            headers={
                "Authorization": f"Bearer {settings.openai_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "prompt": prompt,
                "n": 1,
                "size": "512x512"
            }
        )
        
        if response.status_code != 200:
            logger.error(f"Image generation error: {response.text}")
            return None
        
        data = response.json()
        image_url = data['data'][0]['url']
        
        # Cache results
        await set_cache(cache_key, image_url, 86400)  # 24 hours
        
        return image_url
    except Exception as e:
        logger.error(f"Error generating image: {str(e)}")
        return None