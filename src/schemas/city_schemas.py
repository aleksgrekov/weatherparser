from pydantic import BaseModel, ConfigDict, Field


class CitySchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50, title="Название города")

    model_config = ConfigDict(from_attributes=True)


class ResponseCitySchema(CitySchema):
    id: int = Field(
        ..., title="ID города", description="Уникальный идентификатор города."
    )
