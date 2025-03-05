import asyncio
from typing import Any, Dict, List, Tuple, Sequence, Optional

from sqlalchemy import select, func, asc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.handlers.custom_exceptions import IntegrityViolationException
from src.models.city_model import City
from src.models.weather_model import Weather
from src.parser.funcs import get_weather
from src.repositories.city_repository import CityRepository
from src.schemas.weather_shemas import QueryWeatherSchema, ResponseWeatherWithPaginationSchema, ResponseWeatherSchema


class WeatherRepository:

    @classmethod
    async def get_weather(
            cls, session: AsyncSession, filters: Dict[str, Optional[Any]]
    ) -> ResponseWeatherWithPaginationSchema:
        """
        Получает данные о погоде с учетом фильтров и пагинации.

        :param session: Асинхронная сессия SQLAlchemy.
        :param filters: Объект QueryWeatherSchema с фильтрами.
        :return: Список объектов Weather.
        """

        conditions = cls._build_conditions(filters)

        total_count = await cls._get_total_count(session, conditions)

        limit_value = filters.get("limit") or 10
        page_value = filters.get("page") or 1
        offset_value = (page_value - 1) * limit_value

        query = (
            select(Weather)
            .options(joinedload(Weather.cities))
            .where(*conditions)
            .order_by(asc(Weather.id))
            .limit(limit_value)
            .offset(offset_value)
        )

        request = await session.execute(query)
        response = request.scalars().all()
        return ResponseWeatherWithPaginationSchema(
            total=total_count,
            page=page_value,
            limit=limit_value,
            weather_data=[ResponseWeatherSchema.model_validate(weather) for weather in response],
        )

    @classmethod
    async def add_weather_data(cls, session: AsyncSession) -> bool | None:
        """
        Получает данные о погоде для всех городов и добавляет их в базу данных.
        """
        cities: List["City"] = await CityRepository.get_cities(session)
        if not cities:
            return

        weather_data: Tuple[Dict[str, Any]] = await asyncio.gather(
            *(get_weather(city) for city in cities)
        )
        if not weather_data:
            return

        weather_objects = [Weather(**data) for data in weather_data]
        session.add_all(weather_objects)
        await cls._secure_commit(session)

        return True

    @classmethod
    def _build_conditions(cls, filters: Dict[str, Optional[Any]]) -> Sequence:
        """
        Формирует условия для SQL-запросов на основе переданных фильтров.

        :param filters: Словарь фильтров.
        :return: Список условий для SQLAlchemy.
        """
        filters_list = []
        for key, value in filters.items():
            if value is not None and key not in ("page", "limit"):
                if key == "start_time":
                    filters_list.append(getattr(Weather, "timestamp") >= value)
                elif key == "end_time":
                    filters_list.append(getattr(Weather, "timestamp") <= value)
                elif key == "city_title":
                    filters_list.append(Weather.city_title == value)
                else:
                    filters_list.append(getattr(Weather, value) == value)

        return filters_list

    @classmethod
    async def _get_total_count(cls, session: AsyncSession, conditions: Sequence) -> int:
        """
        Подсчитывает общее количество записей о погоде, соответствующих условиям.

        :param session: Асинхронная сессия SQLAlchemy.
        :param conditions: Условия для подсчета.
        :return: Количество записей о погоде.
        """
        count_query = select(func.count()).select_from(Weather).where(*conditions)
        return (await session.execute(count_query)).scalar() or 0

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
