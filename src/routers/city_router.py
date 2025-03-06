from typing import Annotated

from fastapi import APIRouter, Path, status

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
    status_code=status.HTTP_201_CREATED,
    summary="Добавить город",
    description="Создает новый город и сохраняет его в базе данных.",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Город успешно добавлен",
            "model": ResponseCitySchema,
        },
        status.HTTP_409_CONFLICT: {
            "description": "Запись с такими данными уже существует!",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Ошибка валидации данных"
        },
    },
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
    status_code=status.HTTP_200_OK,
    summary="Удалить город",
    description="Удаляет город по ID и все связанные с ним данные о погоде.",
    responses={
        status.HTTP_200_OK: {
            "description": "Город успешно удален!",
            "model": SuccessResponse,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Запись с такими данными не существует!",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Ошибка валидации данных"
        },
    },
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
