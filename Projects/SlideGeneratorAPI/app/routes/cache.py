from fastapi import APIRouter, Depends, HTTPException, status
from ..dependencies import get_current_active_user
from ..services import cache_service

router = APIRouter()

@router.delete("/cache/{cache_key}")
async def clear_cache(
    cache_key: str,
    current_user = Depends(get_current_active_user)
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can clear cache"
        )
    return await cache_service.clear_cache(cache_key)