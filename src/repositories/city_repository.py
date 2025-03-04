from sqlalchemy import delete, exists, select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.city_model import City
from src.schemas.base_schemas import SuccessResponse
from src.schemas.city_schemas import CitySchema, ResponseCitySchema
from src.handlers.custom_exceptions import (
    IntegrityViolationException,
    RowAlreadyExistsException,
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

    @staticmethod
    async def get_cities(session: AsyncSession):
        query = select(City.title)
        request: Result = await session.execute(query)
        response = request.scalars().all()
        pass

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
