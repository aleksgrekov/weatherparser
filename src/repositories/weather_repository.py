import asyncio
from typing import List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.handlers.custom_exceptions import IntegrityViolationException
from src.models.city_model import City
from src.models.weather_model import Weather
from src.parser.funcs import get_weather
from src.repositories.city_repository import CityRepository


class WeatherRepository:

    @classmethod
    async def get_weather_data(cls, session: AsyncSession):
        result = await cls.add_weather_data(session)
        query = select(Weather)
        request = await session.execute(query)
        weather_data = request.scalars().all()
        return result

    @classmethod
    async def add_weather_data(cls, session: AsyncSession) -> bool | None:
        """
        Получает данные о погоде для всех городов и добавляет их в базу данных.
        """
        cities: List["City"] = await CityRepository.get_cities(session)
        if not cities:
            return

        weather_data = await asyncio.gather(*(get_weather(city) for city in cities))
        if not weather_data:
            return

        weather_objects = []
        for data in weather_data:
            new_weather_data = Weather(**data.get("weather"))
            city = await CityRepository.get_city_by_id(session, data.get("city_id"))
            new_weather_data.cities.append(city)
            weather_objects.append(new_weather_data)

        session.add_all(weather_objects)
        await cls._secure_commit(session)

        return True

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
