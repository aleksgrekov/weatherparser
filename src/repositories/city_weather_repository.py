from typing import List

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.handlers.custom_exceptions import RowNotFoundException, IntegrityViolationException
from src.models.city_weather_data_model import CityWeatherData
from src.models.weather_model import WeatherData


class CityWeatherRepository:

    @classmethod
    async def delete_weather_data(cls, session: AsyncSession, city_id: int) -> None:
        weather_data_ids = await cls._get_weather_ids(session, city_id)

        deleted_row = await cls._delete_weather_data_by_id(session, weather_data_ids)
        if not deleted_row:
            raise RowNotFoundException()

        await cls._secure_commit(session)

    @staticmethod
    async def _delete_weather_data_by_id(session: AsyncSession, weather_ids: List[int]) -> bool:
        delete_query = delete(WeatherData).where(WeatherData.id.in_(weather_ids)).returning(WeatherData.id)
        result = await session.execute(delete_query)
        return result.fetchone() is not None

    @staticmethod
    async def _get_weather_ids(session: AsyncSession, city_id: int) -> List[int]:
        query = select(CityWeatherData.weather_id).where(CityWeatherData.city_id == city_id)
        request = await session.execute(query)
        return list(request.scalars().all())

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
