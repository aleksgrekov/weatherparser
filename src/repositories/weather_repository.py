import asyncio
from typing import Any, Dict, List, Optional, Sequence

from sqlalchemy import asc, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.handlers.custom_exceptions import IntegrityViolationException
from src.models.city_model import City
from src.models.weather_model import Weather
from src.parser.funcs import get_weather
from src.repositories.city_repository import CityRepository
from src.schemas.weather_shemas import (
    ResponseWeatherSchema,
    ResponseWeatherWithPaginationSchema,
)


class WeatherRepository:
    """
    Репозиторий для работы с данными о погоде в базе данных.

    Содержит методы для получения, добавления и фильтрации данных о погоде.
    """

    @classmethod
    async def get_weather(
        cls, session: AsyncSession, filters: Dict[str, Optional[Any]]
    ) -> ResponseWeatherWithPaginationSchema:
        """
        Получает данные о погоде с учетом фильтров и пагинации.

        :param session: Асинхронная сессия SQLAlchemy.
        :param filters: Словарь фильтров для запроса.
        :return: Схема ответа с данными о погоде и пагинацией.
        """
        conditions = cls._build_conditions(filters)

        # Получаем общее количество записей для пагинации
        total_count = await cls._get_total_count(session, conditions)

        # Извлекаем параметры пагинации (по умолчанию: limit=10, page=1)
        limit_value = filters.get("limit") or 10
        page_value = filters.get("page") or 1
        offset_value = (page_value - 1) * limit_value

        # Формируем SQL-запрос с учетом фильтров и пагинации
        query = (
            select(Weather)
            .options(joinedload(Weather.cities))  # Загружаем связанные города
            .where(*conditions)  # Применяем условия фильтрации
            .order_by(asc(Weather.id))  # Сортируем по id
            .limit(limit_value)  # Ограничиваем количество записей
            .offset(offset_value)  # Пропускаем записи для пагинации
        )

        # Выполняем запрос
        request = await session.execute(query)
        response = request.scalars().all()

        # Формируем и возвращаем ответ с пагинацией
        return ResponseWeatherWithPaginationSchema(
            total=total_count,
            page=page_value,
            limit=limit_value,
            weather_data=[
                ResponseWeatherSchema.model_validate(weather) for weather in response
            ],
        )

    @classmethod
    async def add_weather_data(cls, session: AsyncSession) -> Optional[bool]:
        """
        Получает данные о погоде для всех городов и добавляет их в базу данных.

        :param session: Асинхронная сессия SQLAlchemy.
        :return: True, если данные добавлены, иначе None.
        """
        semaphore = asyncio.Semaphore(10)  # Ограничиваем до 10 одновременных запросов

        cities: List[City] = await CityRepository.get_cities(session)
        if not cities:
            return None

        # Получаем данные о погоде для каждого города
        weather_data = await asyncio.gather(
            *(cls._get_weather_with_limit(city, semaphore) for city in cities)
        )
        if not weather_data:
            return None

        # Создаем объекты Weather для каждого города и данных о погоде
        weather_objects = [Weather(**data) for data in weather_data if data is not None]

        # Добавляем их в сессию
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
        # Маппинг фильтров на поля модели
        filter_map = {
            "start_time": lambda value: getattr(Weather, "timestamp") >= value,
            "end_time": lambda value: getattr(Weather, "timestamp") <= value,
            "city_title": lambda value: Weather.city_title == value,
        }

        # Создаем список условий, применяя фильтры
        filters_list = [
            (
                filter_map[key](value)
                if key in filter_map
                else getattr(Weather, key) == value
            )
            for key, value in filters.items()
            if value is not None and key not in ("page", "limit")
        ]

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
    async def _get_weather_with_limit(cls, city: City, semaphore: asyncio.Semaphore):
        async with semaphore:  # Ограничиваем число одновременных запросов
            return await get_weather(city)

    @classmethod
    async def _secure_commit(cls, session: AsyncSession) -> None:
        """
        Безопасно выполняет commit в базу данных с обработкой исключений.

        :param session: Асинхронная сессия SQLAlchemy.
        :raises IntegrityViolationException: Если произошла ошибка при добавлении данных.
        """
        try:
            await session.commit()
        except IntegrityError as exc:
            await session.rollback()
            raise IntegrityViolationException(
                f"Ошибка при добавлении данных о погоде: {exc}"
            )
