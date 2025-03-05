from typing import Type

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

    @classmethod
    async def add_new_city(
            cls, session: AsyncSession, city_data: CitySchema
    ) -> ResponseCitySchema:
        city_title = city_data.title
        if await cls._city_exists(session, city_title):
            raise RowAlreadyExistsException()

        new_city = City(**city_data.model_dump())
        session.add(new_city)
        await cls._secure_commit(session)
        return ResponseCitySchema.model_validate(new_city)

    @classmethod
    async def delete_city(cls, session: AsyncSession, city_id: int) -> SuccessResponse:
        deleted_city = await cls._delete_city_by_id(session, city_id)
        if not deleted_city:
            raise RowNotFoundException()

        await cls._secure_commit(session)
        return SuccessResponse(message="Город успешно удален!")

    @staticmethod
    async def get_cities(session: AsyncSession):
        query = select(City)
        request = await session.execute(query)
        return request.scalars().all()

    @staticmethod
    async def get_city_by_id(session: AsyncSession, city_id: int) -> Type[City]:
        city = await session.get(City, city_id)
        if city is not None:
            return city

    @staticmethod
    async def _city_exists(session: AsyncSession, city_title: str) -> bool:
        """
        Проверка существования города по названию.
        """
        exists_query = select(exists().where(City.title == city_title))
        return await session.scalar(exists_query)

    @staticmethod
    async def _delete_city_by_id(session: AsyncSession, city_id: int) -> bool:
        """
        Удаление города по ID с возвращением ID удаленной записи.
        """
        delete_query = delete(City).where(City.id == city_id).returning(City.id)
        result = await session.execute(delete_query)
        return result.fetchone() is not None

    @staticmethod
    async def _secure_commit(session: AsyncSession) -> None:
        """
        Безопасно выполняет commit в базу данных.
        """
        try:
            await session.commit()
        except IntegrityError as exc:
            await session.rollback()
            raise IntegrityViolationException(str(exc))
