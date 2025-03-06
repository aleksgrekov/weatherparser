from fastapi import APIRouter, Depends, status

from src.database.service import DBSession
from src.repositories.weather_repository import WeatherRepository
from src.schemas.weather_shemas import (
    QueryWeatherSchema,
    ResponseWeatherWithPaginationSchema,
)

router = APIRouter(
    prefix="/weather",
    tags=["WEATHER"],
)


@router.get(
    "/",
    response_model=ResponseWeatherWithPaginationSchema,
    status_code=status.HTTP_200_OK,
    summary="Получить данные о погоде",
    description="Возвращает данные о погоде с возможностью фильтрации по городу, диапазону времени и пагинации.",
    responses={
        status.HTTP_200_OK: {
            "description": "Данные о погоде получены!",
            "model": ResponseWeatherWithPaginationSchema,
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Ошибка валидации данных"
        },
    },
)
async def get_weather(
    session: DBSession,
    query_params: QueryWeatherSchema = Depends(),
) -> ResponseWeatherWithPaginationSchema:
    """
    Получает данные о погоде с учетом фильтров.

    - **query_params**: Фильтры запроса (город, временной диапазон, лимит, офсет)
    - **session**: Асинхронная сессия базы данных
    """
    params = query_params.model_dump()
    return await WeatherRepository.get_weather(session, params)
