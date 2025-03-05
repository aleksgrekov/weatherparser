from datetime import datetime
from typing import List

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import Base
from src.models.city_model import City


class WeatherData(Base):
    __tablename__ = "weather_data"

    timestamp: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now
    )
    description: Mapped[str] = mapped_column(String(50))
    temperature: Mapped[float]
    wind_speed: Mapped[float]

    cities: Mapped[List["City"]] = relationship(
        secondary="CityWeatherData",
        back_populates="weather",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
