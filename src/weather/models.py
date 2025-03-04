from datetime import datetime, timezone

from sqlalchemy import Float, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base_model import Base


class WeatherData(Base):
    __tablename__ = "weather_data"

    timestamp: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), default=datetime.now(timezone.utc)
    )
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    wind_speed: Mapped[float] = mapped_column(Float, nullable=False)
    precipitation: Mapped[float] = mapped_column(Float, nullable=False)

    cities = relationship("CityWeatherData", back_populates="weather")
