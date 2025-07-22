from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..services import auth_service
from ..models.schemas import Token, UserCreate

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    return await auth_service.login(form_data)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    return await auth_service.register(user)