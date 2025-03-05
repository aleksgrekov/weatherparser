from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import Base


class Weather(Base):
    __tablename__ = "weather"

    temperature: Mapped[float]
    wind_speed: Mapped[float]
    description: Mapped[str] = mapped_column(String(50))
    timestamp: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now
    )

    cities = relationship(
        "City",
        secondary="city_weather",
        back_populates="weather",
        cascade="all, delete",
        passive_deletes=True,
    )
