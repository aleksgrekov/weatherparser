from pydantic import BaseModel, Field


class ErrorResponseSchema(BaseModel):
    """
    Схема для ответа об ошибке. Используется для отправки информации о возникшей ошибке.
    """

    type: str = Field(
        ...,
        title="Тип ошибки",
        description="Тип ошибки, например, 'ValidationError' или 'InternalServerError'.",
    )
    message: str = Field(
        ...,
        title="Сообщение об ошибке",
        description="Сообщение, содержащее подробности об ошибке.",
    )
