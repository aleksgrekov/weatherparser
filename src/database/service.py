from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.database.config import db_settings
from src.models.base_model import Base

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


async def create_tables() -> None:
    """
    Создает все таблицы в базе данных на основе объявленных моделей.
    """
    print("Начало создания таблиц...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Таблицы успешно созданы")


async def delete_tables() -> None:
    """
    Удаляет все таблицы из базы данных.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Аннотированный тип для внедрения зависимостей FastAPI
DBSession = Annotated[AsyncSession, Depends(get_session)]
