import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.database.service import create_tables, delete_tables
from src.parser.scheduler import start_scheduler
from src.routers.base_router import router as base_router
from src.middleware.requests_log_mw import create_request_logger_middleware


@asynccontextmanager
async def lifespan(fast_api: FastAPI):
    # Очистка базы данных и создание таблиц
    await delete_tables()
    print("База данных очищена")

    await create_tables()
    print("База данных готова к работе")

    scheduler_task = asyncio.create_task(start_scheduler())
    yield
    scheduler_task.cancel()
    print("Завершение работы приложения")


# Создание экземпляра FastAPI
app = FastAPI(
    title="API Парсинга Погоды",
    version="1.0.0",
    lifespan=lifespan
)

# Подключение роутеров
app.include_router(base_router)
app.add_middleware(create_request_logger_middleware())

if __name__ == "__main__":
    uvicorn.run("main:app")
