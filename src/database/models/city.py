from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    weather_data = relationship(
        "CityWeatherData",
        foreign_keys="CityWeatherData.city_id",
        back_populates="city",
        cascade="all, delete-orphan",
    )
