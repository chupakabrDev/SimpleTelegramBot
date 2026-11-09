from datetime import date

from sqlalchemy import Date, String
from sqlalchemy.orm import (
    Mapped, mapped_column,
)

from repository import Base, KeyedMixin


class User(KeyedMixin, Base):
    __tablename__ = "users"

    registration_date: Mapped[date] = mapped_column(Date)
    name: Mapped[str] = mapped_column(String(100))
    surname: Mapped[str] = mapped_column(String(100))

    def __str__(self) -> str:
        return (
            f"User(key={self.key}, {self.name} {self.surname}, "
            f"registered={self.registration_date:%Y-%m-%d})"
        )
