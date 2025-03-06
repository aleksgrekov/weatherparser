from pydantic import BaseModel, ConfigDict, Field, field_validator


class CitySchema(BaseModel):
    """
    Схема для представления города.
    Используется для описания основных данных о городе, таких как его название.
    """

    title: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[A-Za-zА-Яа-яЁё\s-]+$",
        title="Название города",
        description="Название города. Должно быть длиной от 3 до 50 символов, "
        "состоять из букв, разрешены пробелы и дефисы",
    )

    @field_validator("title", mode="before")
    @classmethod
    def transform(cls, value: str) -> str:
        return value.title()


class ResponseCitySchema(CitySchema):
    """
    Схема для ответа, включающего данные о городе с его уникальным идентификатором.
    Наследуется от CitySchema и добавляет поле для идентификатора города.
    """

    id: int = Field(
        ...,
        title="ID города",
        description="Уникальный идентификатор города, присваиваемый при его создании в базе данных.",
    )

    model_config = ConfigDict(from_attributes=True)
