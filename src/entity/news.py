from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from repository import Base, KeyedMixin


class News(KeyedMixin, Base):
    __tablename__ = "news"

    author: Mapped[int] = mapped_column(ForeignKey("users.key"), index=True)
    creation_date: Mapped[datetime] = mapped_column(DateTime)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)

    def __str__(self) -> str:
        return (
            f"News(key={self.key}, author={self.author}, "
            f"created={self.creation_date:%Y-%m-%d %H:%M}, title={self.title!r})"
        )