from datetime import datetime

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import Base


class Weather(Base):
    """
    Модель записей о погоде.

    Хранит данные о температуре, скорости ветра, описании погоды и времени записи.
    """

    __tablename__ = "weather"

    temperature: Mapped[float]  # Температура воздуха
    wind_speed: Mapped[float]  # Скорость ветра
    description: Mapped[str] = mapped_column(String(50))  # Описание погодных условий
    timestamp: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now
    )  # Временная метка записи
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id", ondelete="CASCADE")
    )  # ID города

    cities = relationship(
        "City",
        back_populates="weather",
    )  # Связь с моделью города

    city_title: AssociationProxy[str] = association_proxy(
        "cities", "title"
    )  # Прокси для получения названия города
