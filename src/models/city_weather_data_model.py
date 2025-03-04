from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import Base


# class CityWeatherData(Base):
#     __tablename__ = "city_weather_data"
#     __table_args__ = (
#         UniqueConstraint(
#             "city_id",
#             "weather_id",
#             name="idx_unique_city_weather",
#         ),
#     )
#
#     city_id: Mapped[int] = mapped_column(ForeignKey("cities.id", ondelete="CASCADE"))
#     weather_id: Mapped[int] = mapped_column(
#         ForeignKey("weather_data.id", ondelete="CASCADE")
#     )
#
#     city = relationship("City", back_populates="weather_data", passive_deletes=True)
#     weather = relationship(
#         "WeatherData",
#         back_populates="cities",
#         passive_deletes=True,
#     )

class CityWeatherData(Base):
    __tablename__ = "city_weather_data"
    __table_args__ = (
        UniqueConstraint(
            "city_id",
            "weather_id",
            name="idx_unique_city_weather",
        ),
    )

    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id", ondelete="CASCADE"), nullable=False)
    weather_id: Mapped[int] = mapped_column(ForeignKey("weather_data.id", ondelete="CASCADE"), nullable=False)

    city = relationship(
        "City",
        back_populates="weather_data",
        passive_deletes=True
    )
    weather = relationship(
        "WeatherData",
        back_populates="cities",
        passive_deletes=True
    )
