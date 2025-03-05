from datetime import datetime

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
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
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id", ondelete="CASCADE"))

    cities = relationship(
        "City",
        back_populates="weather",
    )

    city_title: AssociationProxy[str] = association_proxy(
        "cities", "title"
    )
