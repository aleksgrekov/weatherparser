from fastapi import APIRouter, Depends

from src.database.service import DBSession
from src.repositories.weather_repository import WeatherRepository
from src.schemas.weather_shemas import QueryWeatherSchema, ResponseWeatherWithPaginationSchema

router = APIRouter(
    prefix="/weather",
    tags=["WEATHER"],
)


@router.get("/")
async def get_weather(
    session: DBSession,
    query_params: QueryWeatherSchema = Depends(),
) -> ResponseWeatherWithPaginationSchema:
    params = query_params.model_dump()
    return await WeatherRepository.get_weather(session, params)
