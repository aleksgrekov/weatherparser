from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import Base


class City(Base):
    __tablename__ = "cities"

    title: Mapped[str] = mapped_column(String(50), unique=True)

    weather = relationship(
        "Weather",
        back_populates="cities",
        cascade="all, delete",
        passive_deletes=True,
    )
