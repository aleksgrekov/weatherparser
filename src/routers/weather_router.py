from fastapi import APIRouter

from src.database.service import DBSession
from src.repositories.weather_repository import WeatherRepository

router = APIRouter(
    prefix="/api/weather",
    tags=["WEATHER"],
)


@router.get("/")
async def get_weather(session: DBSession):
    return await WeatherRepository.get_weather_data(session)
