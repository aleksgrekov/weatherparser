from sqlalchemy import select, exists, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.city.models import City
from src.city.schemas import CitySchema, ResponseCitySchema, SuccessResponse
from src.handlers.custom_exceptions import (
    RowAlreadyExistsException,
    IntegrityViolationException,
    RowNotFoundException,
)


class CityRepository:

    @classmethod
    async def add_new_city(
        cls, session: AsyncSession, city_data: CitySchema
    ) -> ResponseCitySchema:
        city_title = city_data.title
        if city_title and await session.scalar(
            select(exists().where(City.title == city_title))
        ):
            raise RowAlreadyExistsException()

        new_city = City(**city_data.model_dump())

        session.add(new_city)
        await cls._secure_commit(session)
        return ResponseCitySchema.model_validate(new_city)

    @classmethod
    async def delete_city(cls, session: AsyncSession, city_id: int) -> SuccessResponse:
        delete_query = delete(City).returning(City.id).where(City.id == city_id)
        request = await session.execute(delete_query)

        if not request.fetchone():
            raise RowNotFoundException()

        await cls._secure_commit(session)
        return SuccessResponse(message="Город успешно удален!")

    @classmethod
    async def _secure_commit(cls, session: AsyncSession) -> None:
        """
        Безопасно выполняет commit в базу данных.
        """
        try:
            await session.commit()
        except IntegrityError as exc:
            await session.rollback()
            raise IntegrityViolationException(str(exc))
