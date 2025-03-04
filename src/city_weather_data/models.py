from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base_model import Base


class CityWeatherData(Base):
    __tablename__ = "city_weather_data"
    __table_args__ = (
        UniqueConstraint(
            "city_id",
            "weather_id",
            name="idx_unique_city_weather",
        ),
    )

    city_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("cities.id", ondelete="CASCADE")
    )
    weather_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("weather_data.id", ondelete="CASCADE")
    )

    city = relationship("City", back_populates="weatherdata")
    weather = relationship("WeatherData", back_populates="cities")
