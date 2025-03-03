from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.database.config import settings
from src.database.base_model import Base
from src.city.models import City
from src.weather.models import WeatherData
from src.city_weather_data.models import CityWeatherData

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
