import redis
from app.core.config import settings
from app.core.logging import logger

class RedisCache:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            try:
                cls._instance.client = redis.Redis.from_url(
                    settings.REDIS_URL, 
                    decode_responses=True,
                    socket_timeout=3,
                    socket_connect_timeout=3
                )
                cls._instance.client.ping()
                logger.info("Redis connection established")
            except redis.ConnectionError:
                logger.warning("Redis connection failed, using in-memory cache")
                cls._instance.client = None
                cls._instance.memory_cache = {}
        return cls._instance
    
    def get(self, key: str):
        if self.client:
            try:
                return self.client.get(key)
            except redis.RedisError:
                return None
        return self.memory_cache.get(key)
    
    def set(self, key: str, value: str, ttl: int = None):
        if self.client:
            try:
                self.client.set(key, value, ex=ttl or settings.CACHE_TTL)
                return True
            except redis.RedisError:
                return False
        self.memory_cache[key] = value
        return True
    
    def delete(self, key: str):
        if self.client:
            try:
                return self.client.delete(key)
            except redis.RedisError:
                return 0
        if key in self.memory_cache:
            del self.memory_cache[key]
            return 1
        return 0
    
    def acquire_lock(self, lock_key: str, timeout: int = 10):
        if self.client:
            return self.client.set(lock_key, "locked", nx=True, ex=timeout)
        return lock_key not in self.memory_cache
    
    def release_lock(self, lock_key: str):
        if self.client:
            self.client.delete(lock_key)
        elif lock_key in self.memory_cache:
            del self.memory_cache[lock_key]

cache = RedisCache()