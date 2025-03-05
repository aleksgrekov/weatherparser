from typing import Annotated

from fastapi import APIRouter, Path

from src.database.service import DBSession
from src.repositories.city_repository import CityRepository
from src.schemas.base_schemas import SuccessResponse
from src.schemas.city_schemas import CitySchema, ResponseCitySchema

router = APIRouter(
    prefix="/cities",
    tags=["CITY"],
)


@router.post(
    "/",
    response_model=ResponseCitySchema,
    summary="Добавить город",
    description="Создает новый город и сохраняет его в базе данных.",
)
async def add_city(session: DBSession, city_data: CitySchema) -> ResponseCitySchema:
    """
    Добавляет новый город в базу данных.

    - **city_data**: Данные о городе
    - **session**: Асинхронная сессия базы данных
    """
    return await CityRepository.add_new_city(session, city_data)


@router.delete(
    "/{city_id}",
    response_model=SuccessResponse,
    summary="Удалить город",
    description="Удаляет город по ID и все связанные с ним данные о погоде.",
)
async def delete_city(
    session: DBSession, city_id: Annotated[int, Path(ge=1)]
) -> SuccessResponse:
    """
    Удаляет город из базы данных по ID.

    - **city_id**: Уникальный идентификатор города (должен быть >= 1)
    - **session**: Асинхронная сессия базы данных
    """
    return await CityRepository.delete_city(session, city_id)
