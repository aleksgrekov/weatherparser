from fastapi import APIRouter

from src.routers.city_router import router as city_router
from src.routers.weather_router import router as weather_router

router = APIRouter(
    prefix="/api/v1",
)

router.include_router(city_router)
router.include_router(weather_router)
