import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.middleware.requests_log_mw import create_request_logger_middleware
from src.parser.scheduler import start_scheduler
from src.routers.base_router import router as base_router


@asynccontextmanager
async def lifespan(fast_api: FastAPI):
    scheduler_task = asyncio.create_task(start_scheduler())
    yield
    scheduler_task.cancel()


# Создание экземпляра FastAPI
app = FastAPI(title="API Парсинга Погоды", version="1.0.0", lifespan=lifespan)

# Подключение роутеров
app.include_router(base_router)
app.add_middleware(create_request_logger_middleware())
