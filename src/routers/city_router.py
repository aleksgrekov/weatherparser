from typing import Annotated

from fastapi import APIRouter, Path

from src.database.service import DBSession
from src.repositories.city_repository import CityRepository
from src.schemas.city_schemas import CitySchema

router = APIRouter(
    prefix="/cities",
    tags=["CITY"],
)


@router.post("/")
async def add_city(session: DBSession, city_data: CitySchema):
    return await CityRepository.add_new_city(session, city_data)


@router.delete("/{city_id}")
async def delete_city(session: DBSession, city_id: Annotated[int, Path(ge=1)]):
    return await CityRepository.delete_city(session, city_id)
