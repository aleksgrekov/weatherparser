from fastapi import APIRouter

router = APIRouter(
    prefix="/api/city",
    tags=["CITY"],
)


@router.post("/")
async def add_city():
    pass
