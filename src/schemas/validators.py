# validators.py
from pydantic import field_validator

from src.handlers.custom_exceptions import WrongDataException


# Валидатор для проверки порядка времени (start_time <= end_time)
def check_time_order(start_time, end_time) -> None:
    if start_time and end_time and start_time > end_time:
        raise WrongDataException("Поле start_time не может быть больше end_time!")


# Валидатор для преобразования строки city_title в заглавные буквы
def transform_city_title(cls, value: str) -> str:
    if value is not None:
        return value.title()
