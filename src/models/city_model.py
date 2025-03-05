from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import Base
from src.models.weather_model import WeatherData


class City(Base):
    __tablename__ = "cities"

    title: Mapped[str] = mapped_column(String(50), unique=True)

    weather: Mapped[List["WeatherData"]] = relationship(
        secondary="CityWeatherData",
        back_populates="cities",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
