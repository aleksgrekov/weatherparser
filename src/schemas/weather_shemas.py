from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


class QueryWeatherSchema(BaseModel):
    city_title: Optional[str] = Field(
        None,
        min_length=3,
        max_length=50,
        title="Название города",
    )
    start_time: Optional[datetime] = Field(
        None, title="Записи о погоде не ранее заданного времени"
    )
    end_time: Optional[datetime] = Field(
        None, title="Записи о погоде не позднее заданного времени"
    )
    page: Optional[int] = Field(
        default=1,
        ge=1,
        title="Страница",
        description="Номер страницы для пагинации. Значение должно быть больше или равно 1.",
    )
    limit: Optional[int] = Field(
        default=10,
        ge=1,
        title="Лимит",
        description="Количество записей на одной странице. Значение должно быть больше или равно 1.",
    )


class ResponseWeatherSchema(BaseModel):
    temperature: float = Field(
        ...,
    )
    wind_speed: float = Field(
        ...,
    )
    description: str = Field(
        ...,
        max_length=50,
    )
    timestamp: datetime = Field(
        ...,
    )
    city_id: int = Field(
        ...,
    )
    city_title: str = Field(
        ...,
        title="Название города",
        description="Название города, к которому принадлежит запись о погоде.",
    )

    model_config = ConfigDict(from_attributes=True)


class ResponseWeatherWithPaginationSchema(BaseModel):
    """
    Схема для ответа с пагинированным списком записей о погоде.
    """

    total: int = Field(
        ...,
        title="Общее количество записей",
        description="Общее количество записей.",
    )
    page: int = Field(
        ...,
        title="Текущая страница",
        description="Номер текущей страницы с результатами.",
    )
    limit: int = Field(
        ...,
        title="Лимит на странице",
        description="Количество записей на одной странице.",
    )
    weather_data: List[ResponseWeatherSchema] = Field(
        ...,
        title="Список записей",
        description="Список записей на текущей странице.",
    )

