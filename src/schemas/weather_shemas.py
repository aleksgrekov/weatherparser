from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from src.schemas.validators import check_time_order, transform_city_title


class QueryWeatherSchema(BaseModel):
    """
    Схема для запроса данных о погоде.
    Позволяет фильтровать данные о погоде по городу, времени и пагинации.
    """

    city_title: Optional[str] = Field(
        None,
        min_length=3,
        max_length=50,
        pattern=r"^[A-Za-zА-Яа-яЁё\s-]+$",
        title="Название города",
        description="Название города, для которого необходимо получить данные о погоде. "
        "Должно быть длиной от 3 до 50 символов, состоять из букв, разрешены пробелы и дефисы",
    )
    start_time: Optional[datetime] = Field(
        None,
        title="Записи о погоде не ранее заданного времени",
        description="Фильтрация по времени начала записи погоды. "
        "Если указано, возвращаются записи о погоде, начиная с этого времени.",
    )
    end_time: Optional[datetime] = Field(
        None,
        title="Записи о погоде не позднее заданного времени",
        description="Фильтрация по времени окончания записи погоды. "
        "Если указано, возвращаются записи о погоде, заканчивающиеся до этого времени.",
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

    @model_validator(mode="after")
    def check_time_order(self) -> "QueryWeatherSchema":
        check_time_order(self.start_time, self.end_time)
        return self

    validation_field = field_validator("city_title", mode="before")(
        transform_city_title
    )


class ResponseWeatherSchema(BaseModel):
    """
    Схема для представления записи о погоде.
    Включает данные о температуре, скорости ветра, описании погоды и времени записи.
    """

    temperature: float = Field(
        ...,
        title="Температура",
        description="Температура воздуха, измеренная в градусах Цельсия.",
    )
    wind_speed: float = Field(
        ..., title="Скорость ветра", description="Скорость ветра в метрах в секунду."
    )
    description: str = Field(
        ...,
        max_length=50,
        title="Описание погоды",
        description="Краткое описание погодных условий, например, 'пасмурно', 'переменная облачность'.",
    )
    timestamp: datetime = Field(
        ...,
        title="Время записи",
        description="Время, когда была сделана запись о погоде.",
    )
    city_id: int = Field(
        ...,
        title="ID города",
        description="Уникальный идентификатор города, к которому относится запись о погоде.",
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
    Включает информацию о пагинации, а также список записей о погоде.
    """

    total: int = Field(
        ...,
        title="Общее количество записей",
        description="Общее количество записей о погоде, соответствующих запросу.",
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
        description="Список записей о погоде на текущей странице.",
    )
