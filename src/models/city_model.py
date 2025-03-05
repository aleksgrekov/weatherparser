from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import Base


class City(Base):
    """
    Модель города.

    Содержит информацию о городе и связь с таблицей погоды.
    """

    __tablename__ = "cities"

    title: Mapped[str] = mapped_column(String(50), unique=True)  # Название города

    weather = relationship(
        "Weather",
        back_populates="cities",
        cascade="all, delete",
        passive_deletes=True,
    )  # Связь с моделью записей о погоде
