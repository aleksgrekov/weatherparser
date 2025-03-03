from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base_model import Base


class City(Base):
    __tablename__ = "cities"

    title: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    weather_data = relationship(
        "CityWeatherData",
        foreign_keys="CityWeatherData.city_id",
        back_populates="city",
        cascade="all, delete-orphan",
    )
