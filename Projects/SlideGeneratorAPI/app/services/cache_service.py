from ..utils.cache import clear_cache as clear_cache_util

async def clear_cache(cache_key: str):
    result = await clear_cache_util(cache_key)
    return {"status": "success", "deleted": result}