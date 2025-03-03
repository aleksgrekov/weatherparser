from pydantic import BaseModel, Field, ConfigDict


class SuccessResponse(BaseModel):
    """
    Схема для успешного ответа. Используется для передачи подтверждения выполнения операции.
    """

    message: str = Field(
        ...,
        title="Сообщение об успехе",
        description="Сообщение, подтверждающее успешное выполнение операции.",
    )


class CitySchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50, title="Название города")

    model_config = ConfigDict(from_attributes=True)


class ResponseCitySchema(CitySchema):
    id: int = Field(
        ..., title="ID города", description="Уникальный идентификатор города."
    )
