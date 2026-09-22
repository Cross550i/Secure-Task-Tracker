import bcrypt
from datetime import datetime, timezone, timedelta

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.config import settings
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.models import User
from src.database import get_async_db


security_scheme = HTTPBearer()


async def get_current_user(token: HTTPAuthorizationCredentials = Depends(security_scheme), db: AsyncSession = Depends(get_async_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось валидировать учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        raw_token = token.credentials
        payload = jwt.decode(raw_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    user_base = result.scalars().one_or_none()
    if user_base is None:
        raise credentials_exception
    return user_base


def get_password_hash(password: str) -> str:
    """
    Принимает чистый пароль (строку), кодирует её в байты,
    генерирует соль, хеширует и возвращает строку-хеш.
    """
    # 1. Переводим строку пароля в байты (UTF-8)
    password_bytes = password.encode('utf-8')

    # 2. Генерируем случайную "соль" для защиты от подбора по словарям
    salt = bcrypt.gensalt()

    # 3. Хешируем пароль вместе с солью
    hashed_password_bytes = bcrypt.hashpw(password_bytes, salt)

    # 4. Декодируем байты обратно в читаемую строку для сохранения в БД
    return hashed_password_bytes.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Сравнивает чистый пароль, введенный пользователем,
    с хешем, сохраненным в базе данных.
    """
    # Переводим обе строки в байты для сравнения библиотекой bcrypt
    plain_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')

    # Безопасно сравниваем пароль и хеш
    return bcrypt.checkpw(plain_bytes, hashed_bytes)


def create_access_token(data: dict) -> str:
    data_copy = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    data_copy["exp"] = expire
    result = jwt.encode(data_copy, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return result
