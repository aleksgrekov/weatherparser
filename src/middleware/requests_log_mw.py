from fastapi import Request
from datetime import datetime

from starlette.middleware.base import BaseHTTPMiddleware

from src.logger.logger import get_logger

logger = get_logger(__name__)


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    """
    Middleware для логирования информации о запросах.
    Логирует метод, URL и время запроса.
    """

    async def dispatch(self, request: Request, call_next):
        # Логируем информацию о запросе
        method = request.method
        url = str(request.url)
        start_time = datetime.now()

        logger.info(f"Запрос: {method} {url} - Начало")

        # Обрабатываем запрос
        response = await call_next(request)

        # Логируем время выполнения
        end_time = datetime.now()
        elapsed_time = (end_time - start_time).total_seconds()

        logger.info(
            f"Запрос: {method} {url} - Ответ код {response.status_code} - Время выполнения: {elapsed_time:.4f} сек.")

        return response


def create_request_logger_middleware():
    return RequestLoggerMiddleware
