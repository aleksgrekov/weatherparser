import asyncio
from typing import Any, Dict, List, Tuple

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.handlers.custom_exceptions import IntegrityViolationException
from src.models.city_model import City
from src.models.city_weather_data_model import CityWeatherData
from src.models.weather_model import WeatherData
from src.parser.funcs import get_weather
from src.repositories.city_repository import CityRepository


class WeatherRepository:

    @classmethod
    async def get_weather_data(cls, session: AsyncSession):
        result = await cls.add_weather_data(session)
        query = select(WeatherData)
        request = await session.execute(query)
        weather_data = request.scalars().all()
        return result

    @classmethod
    async def add_weather_data(cls, session: AsyncSession) -> bool | None:
        """
        Получает данные о погоде для всех городов и добавляет их в базу данных.
        """
        weather_data = await cls._fetch_weather_for_cities(session)

        if not weather_data:
            return

        city_weather_data_objects = []
        for data in weather_data:
            new_weather_data = WeatherData(**data.get("weather"))
            session.add(new_weather_data)
            await session.flush()

            city_id, weather_id = data.get("city_id"), new_weather_data.id
            city_weather_data_objects.append(
                CityWeatherData(city_id=city_id, weather_id=weather_id)
            )

        session.add_all(city_weather_data_objects)
        await cls._secure_commit(session)

        return True

    @classmethod
    async def _fetch_weather_for_cities(
        cls, session: AsyncSession
    ) -> Tuple[Dict[str, Any]] | None:
        """
        Получает данные о погоде для всех городов из базы данных.
        """
        cities: List["City"] = await CityRepository.get_cities(session)

        if not cities:
            return None

        weather_data = await asyncio.gather(*(get_weather(city) for city in cities))
        return weather_data

    @classmethod
    async def _secure_commit(cls, session: AsyncSession) -> None:
        """
        Безопасно выполняет commit в базу данных с обработкой исключений.
        """
        try:
            await session.commit()
        except IntegrityError as exc:
            await session.rollback()
            raise IntegrityViolationException(
                f"Ошибка при добавлении данных о погоде: {exc}"
            )
