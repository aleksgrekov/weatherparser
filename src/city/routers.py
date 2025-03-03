from typing import Annotated

from fastapi import APIRouter, Path

from src.city.repositories import CityRepository
from src.city.schemas import CitySchema
from src.database.service import DBSession

router = APIRouter(
    prefix="/api/city",
    tags=["CITY"],
)


@router.post("/")
async def add_city(session: DBSession, city_data: CitySchema):
    return await CityRepository.add_new_city(session, city_data)


@router.delete("/{city_id}")
async def delete_city(session: DBSession, city_id: Annotated[int, Path(ge=1)]):
    return await CityRepository.delete_city(session, city_id)
