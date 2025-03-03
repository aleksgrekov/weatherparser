from datetime import datetime, timezone

from sqlalchemy import Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import Base


class WeatherData(Base):
    __tablename__ = "weather_data"

    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(timezone.utc)
    )
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    wind_speed: Mapped[float] = mapped_column(Float, nullable=False)
    precipitation: Mapped[float] = mapped_column(Float, nullable=False)

    cities = relationship("CityWeatherData", back_populates="weather")
