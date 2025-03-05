from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.database.config import db_settings
from src.models.base_model import Base

# Создаем движок
DB_URL = db_settings.db_url(driver="asyncpg")
engine = create_async_engine(DB_URL, echo=False)

# Фабрика сессий
API_SessionFactory = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)

Scheduler_SessionFactory = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронный генератор сессии БД."""
    async with API_SessionFactory() as session:
        yield session


async def create_tables():
    print("Начало создания таблиц...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Таблицы успешно созданы")


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Используется для внедрения зависимостей в FastAPI
DBSession = Annotated[AsyncSession, Depends(get_session)]
