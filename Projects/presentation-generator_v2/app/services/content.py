import json
import logging
import asyncio
import hashlib
from app.core.config import settings
from app.models.presentation import PresentationCreate, SlideContent
from app.utils.redis import cache
from tenacity import retry, stop_after_attempt, wait_exponential
from openai import AsyncOpenAI
from app.core.exceptions import ContentGenerationException

logger = logging.getLogger(__name__)

class ContentService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.semaphore = asyncio.Semaphore(settings.MAX_CONCURRENT_GENERATIONS)
    
    async def generate_content(self, request: PresentationCreate) -> list[SlideContent]:
        cache_key = self._get_cache_key(request)
        
        if cached := cache.get(cache_key):
            logger.info(f"Cache hit for key: {cache_key}")
            return self._deserialize_cached_content(cached)
        
        logger.info(f"Cache miss for key: {cache_key}")
        chunks = self._chunk_generation(request)
        results = await asyncio.gather(*chunks)
        
        slides = []
        for chunk in results:
            slides.extend(chunk)
        
        cache.set(cache_key, self._serialize_content(slides))
        return slides

    def _chunk_generation(self, request: PresentationCreate):
        chunks = []
        for i in range(0, request.num_slides, settings.CONTENT_CHUNK_SIZE):
            chunk_size = min(settings.CONTENT_CHUNK_SIZE, request.num_slides - i)
            chunks.append(self._generate_chunk(request.topic, i, chunk_size, request.custom_content))
        return chunks

    async def _generate_chunk(self, topic: str, start_idx: int, chunk_size: int, custom_content: str = None):
        async with self.semaphore:
            try:
                if custom_content:
                    return self._parse_custom_content(custom_content, start_idx, chunk_size)
                
                prompt = self._build_prompt(topic, start_idx, chunk_size)
                return await self._generate_with_retry(prompt)
            except Exception as e:
                logger.error(f"Content generation failed: {str(e)}")
                return [
                    SlideContent(title=f"Slide {start_idx + i + 1}", bullets=["Content generation failed"])
                    for i in range(chunk_size)
                ]

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def _generate_with_retry(self, prompt: str):
        response = await self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        return self._parse_llm_response(content)

    def _get_cache_key(self, request: PresentationCreate) -> str:
        key_data = f"{request.topic}:{request.num_slides}:{request.custom_content or ''}"
        return f"content:{hashlib.sha256(key_data.encode()).hexdigest()}"

    def _serialize_content(self, content: list[SlideContent]) -> str:
        return json.dumps([slide.dict() for slide in content])

    def _deserialize_cached_content(self, cached: str) -> list[SlideContent]:
        data = json.loads(cached)
        return [SlideContent(**item) for item in data]

    def _build_prompt(self, topic: str, start_idx: int, num_slides: int) -> str:
        return f"""
        Generate exactly {num_slides} presentation slides about '{topic}'. 
        Slides should start from number {start_idx + 1}.
        
        For each slide, provide:
        - Title
        - 3-5 bullet points
        - Image suggestion description
        - Source citations (minimum 1 per slide)
        
        Return as strict JSON format:
        {{
            "slides": [
                {{
                    "title": "...",
                    "bullets": ["...", "..."],
                    "image_suggestion": "...",
                    "citations": ["..."]
                }}
            ]
        }}
        """

    def _parse_llm_response(self, response: str) -> list[SlideContent]:
        try:
            data = json.loads(response)
            slides = []
            for slide_data in data["slides"]:
                slides.append(SlideContent(
                    title=slide_data["title"],
                    bullets=slide_data.get("bullets", []),
                    image_suggestion=slide_data.get("image_suggestion", ""),
                    citations=slide_data.get("citations", [])
                ))
            return slides
        except (KeyError, json.JSONDecodeError) as e:
            logger.error(f"JSON parsing failed: {str(e)}")
            raise ContentGenerationException("Failed to parse LLM response")
    
    def _parse_custom_content(self, content: str, start_idx: int, num_slides: int) -> list[SlideContent]:
        return [
            SlideContent(
                title=f"Custom Slide {start_idx + i + 1}",
                bullets=[f"Point {j+1}" for j in range(3)]
            )
            for i in range(num_slides)
        ]