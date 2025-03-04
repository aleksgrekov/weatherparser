import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.database.service import create_tables, delete_tables
from src.parser.scheduler import start_scheduler
from src.routers.city_router import router as city_router
from src.routers.weather_router import router as weather_router


@asynccontextmanager
async def lifespan(fast_api: FastAPI):
    await delete_tables()
    print("База очищена")
    await create_tables()
    print("База готова к работе")

    await asyncio.create_task(start_scheduler())
    yield
    print("Выключение")


# Создание экземпляра FastAPI
app = FastAPI(title="API Парсинга Погоды", version="1.0.0", lifespan=lifespan)

app.include_router(city_router)
app.include_router(weather_router)

if __name__ == "__main__":
    uvicorn.run("main:app")
