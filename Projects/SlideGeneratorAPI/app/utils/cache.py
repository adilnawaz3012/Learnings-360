import redis
import cachetools
from app.core.config import settings

# Cache setup
memory_cache = cachetools.TTLCache(maxsize=1000, ttl=300)
redis_cache = None

async def init_cache():
    global redis_cache
    if not redis_cache:
        redis_cache = redis.Redis.from_url(settings.cache_redis_url)

async def get_cache(key: str):
    # Check memory cache first
    if key in memory_cache:
        return memory_cache[key]
    
    # Then check Redis
    if redis_cache:
        value = redis_cache.get(key)
        if value:
            # Cache in memory for faster access
            memory_cache[key] = value
            return value
    return None

async def set_cache(key: str, value: str, ttl: int = 3600):
    # Set in memory cache
    memory_cache[key] = value
    
    # Set in Redis
    if redis_cache:
        redis_cache.setex(key, ttl, value)

async def clear_cache(key: str):
    # Clear from both caches
    if key in memory_cache:
        del memory_cache[key]
    
    if redis_cache:
        return redis_cache.delete(key)
    return 0

async def close_cache():
    if redis_cache:
        redis_cache.close()