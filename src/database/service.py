from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.database.config import settings
from src.database.models.base import Base
from src.database.models.city import City
from src.database.models.weather_data import WeatherData
from src.database.models.city_weather_data import CityWeatherData

# Создаем движок
DB_URL = settings.db_url(driver="asyncpg")
engine = create_async_engine(DB_URL, echo=False)

# Фабрика сессий
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронный генератор сессии БД."""
    async with async_session() as session:
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
