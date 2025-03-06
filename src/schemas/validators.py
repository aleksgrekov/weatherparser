from datetime import datetime
from typing import Optional

from src.handlers.custom_exceptions import WrongDataException


def check_time_order(
    start_time: Optional[datetime], end_time: Optional[datetime]
) -> None:
    """Валидатор для проверки порядка времени (start_time <= end_time)"""
    if start_time and end_time and start_time > end_time:
        raise WrongDataException("Поле start_time не может быть больше end_time!")


def transform_city_title(value: str) -> str:
    """Валидатор для преобразования строки с названием города в заглавные буквы"""
    if value is not None:
        return value.title()
