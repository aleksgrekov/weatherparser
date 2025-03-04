from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import Base


class WeatherData(Base):
    __tablename__ = "weather_data"

    timestamp: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), default=datetime.now(timezone.utc)
    )
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    wind_speed: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String(50), nullable=False)

    cities = relationship("CityWeatherData", back_populates="weather")
