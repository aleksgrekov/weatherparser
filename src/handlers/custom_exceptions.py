from typing import Optional

from fastapi import HTTPException, status

from src.logger.logger import get_logger

logger = get_logger(__name__)


class BaseCustomException(HTTPException):
    """
    Базовый класс для пользовательских исключений с логированием.
    """

    status_code: int = status.HTTP_400_BAD_REQUEST
    default_message: str = "Произошла ошибка"

    def __init__(self, message: Optional[str] = None):
        detail = message or self.default_message
        super().__init__(status_code=self.status_code, detail=detail)
        logger.warning("%s: %s", self.__class__.__name__, detail)


class RowAlreadyExistsException(BaseCustomException):
    """
    Исключение, возникающее, если запись уже существует в БД.
    """

    status_code = status.HTTP_409_CONFLICT
    default_message = "Запись с такими данными уже существует!"


class RowNotFoundException(BaseCustomException):
    """
    Исключение, возникающее, если запись не существует в БД.
    """

    status_code = status.HTTP_404_NOT_FOUND
    default_message = "Запись с такими данными не существует!"


class IntegrityViolationException(Exception):
    """
    Исключение, возникающее при нарушении целостности данных.
    """

    def __init__(self, message: str):
        super().__init__(message)
