from typing import List, Optional

from sqlalchemy import delete, exists, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.handlers.custom_exceptions import (
    IntegrityViolationException,
    RowAlreadyExistsException,
    RowNotFoundException,
)
from src.models.city_model import City
from src.schemas.base_schemas import SuccessResponse
from src.schemas.city_schemas import CitySchema, ResponseCitySchema


class CityRepository:
    """
    Репозиторий для работы с таблицей городов в базе данных.

    Содержит методы для добавления нового города, удаления города по ID и получения списка всех городов.
    """

    @classmethod
    async def add_new_city(
        cls, session: AsyncSession, city_data: CitySchema
    ) -> ResponseCitySchema:
        """
        Добавляет новый город в базу данных.

        :param session: Асинхронная сессия SQLAlchemy.
        :param city_data: Данные города для добавления.
        :return: Схема ответа с данными добавленного города.
        :raises RowAlreadyExistsException: Если город с таким названием уже существует.
        """
        city_title = city_data.title
        # Проверка на существование города
        if await cls._city_exists(session, city_title):
            raise RowAlreadyExistsException()

        # Создание нового объекта города и добавление его в сессию
        new_city = City(**city_data.model_dump())
        session.add(new_city)
        await cls._secure_commit(session)
        return ResponseCitySchema.model_validate(
            new_city
        )  # Возвращаем схему ответа с данными города

    @classmethod
    async def delete_city(cls, session: AsyncSession, city_id: int) -> SuccessResponse:
        """
        Удаляет город по его ID.

        :param session: Асинхронная сессия SQLAlchemy.
        :param city_id: ID города для удаления.
        :return: Успешный ответ с сообщением.
        :raises RowNotFoundException: Если город с указанным ID не найден.
        """
        if not await cls._delete_city_by_id(session, city_id):
            raise RowNotFoundException()  # Выбрасываем исключение, если город не найден

        await cls._secure_commit(session)  # Обязательный коммит
        return SuccessResponse(
            message="Город успешно удален!"
        )  # Возвращаем успешный ответ

    @staticmethod
    async def get_cities(session: AsyncSession) -> List["City"]:
        """
        Получает список всех городов.

        :param session: Асинхронная сессия SQLAlchemy.
        :return: Список объектов City.
        """
        query = select(City)  # Запрос для получения всех городов
        request = await session.execute(query)
        return list(request.scalars().all())

    @staticmethod
    async def _city_exists(session: AsyncSession, city_title: str) -> Optional[bool]:
        """
        Проверяет, существует ли город с указанным названием.

        :param session: Асинхронная сессия SQLAlchemy.
        :param city_title: Название города.
        :return: True, если город существует, иначе False.
        """
        exists_query = select(
            exists().where(City.title == city_title)
        )  # Запрос для проверки существования города
        return await session.scalar(exists_query)

    @staticmethod
    async def _delete_city_by_id(session: AsyncSession, city_id: int) -> bool:
        """
        Удаляет город по его ID.

        :param session: Асинхронная сессия SQLAlchemy.
        :param city_id: ID города.
        :return: True, если город был удален, иначе False.
        """
        # Запрос на удаление города по ID с возвращением ID удаленного города
        delete_query = delete(City).where(City.id == city_id).returning(City.id)
        result = await session.execute(delete_query)
        return result.fetchone() is not None  # Возвращаем True, если город был удален

    @staticmethod
    async def _secure_commit(session: AsyncSession) -> None:
        """
        Безопасно выполняет commit в базу данных.

        :param session: Асинхронная сессия SQLAlchemy.
        :raises IntegrityViolationException: Если возникает ошибка целостности данных.
        """
        try:
            await session.commit()
        except IntegrityError as exc:  # Обработка ошибок целостности
            await session.rollback()
            raise IntegrityViolationException(str(exc))
