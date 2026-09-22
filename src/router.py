from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_db
from src.schemas import UserResponse, UserCreate, Token
from src.crud import create_user, get_user_by_email
from src.security import verify_password, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_async_db)):
    existing_user = await get_user_by_email(user_data.email, db)
    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Пользователь с таким email уже зарегистрирован")

    created_user = await create_user(user_data, db)
    return created_user


@router.post("/login", response_model=Token)
async def auth(user_data: UserCreate, db: AsyncSession = Depends(get_async_db)):
    existing_user = await get_user_by_email(user_data.email, db)
    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Неверная почта или пароль")

    if not verify_password(user_data.password, existing_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Неверная почта или пароль")

    new_token = create_access_token({"sub": existing_user.email})
    return Token(access_token=new_token, token_type="bearer")
