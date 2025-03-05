from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.database.config import db_settings

# Создаем асинхронный движок базы данных
DB_URL: str = db_settings.db_url(driver="asyncpg")
engine = create_async_engine(DB_URL, echo=False)

# Фабрика сессий для API
API_SessionFactory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)

# Фабрика сессий для планировщика задач (если используется)
Scheduler_SessionFactory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Асинхронный генератор сессии базы данных.

    Используется в качестве зависимости в обработчиках FastAPI.
    """
    async with API_SessionFactory() as session:
        yield session


# Аннотированный тип для внедрения зависимостей FastAPI
DBSession = Annotated[AsyncSession, Depends(get_session)]
