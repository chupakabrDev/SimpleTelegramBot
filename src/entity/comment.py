from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from repository import Base, KeyedMixin


class Comment(KeyedMixin, Base):
    __tablename__ = "comments"

    author: Mapped[int] = mapped_column(ForeignKey("users.key"), index=True)
    news: Mapped[int] = mapped_column(ForeignKey("news.key"), index=True)
    creation_date: Mapped[datetime] = mapped_column(DateTime)
    content: Mapped[str] = mapped_column(Text)

    def __str__(self) -> str:
        return (
            f"Comment(key={self.key}, author={self.author}, news={self.news}, "
            f"created={self.creation_date:%Y-%m-%d %H:%M}, content={self.content!r})"
        )