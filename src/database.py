from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from src.config import settings

engine = create_async_engine(url=settings.database_url,
                             echo=False,
                             pool_size=5,
                             max_overflow=10,
                             future=True,
                             connect_args={"server_settings": {"timezone": "UTC"}}
                             )

async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    pass


async def get_async_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
