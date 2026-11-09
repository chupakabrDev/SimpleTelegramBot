from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from repository import Base, KeyedMixin


class UserLikes(KeyedMixin, Base):
    __tablename__ = "user_likes"
    __table_args__ = (
        UniqueConstraint("news", "user", name="uq_user_likes_news_user"),
    )

    news: Mapped[int] = mapped_column(ForeignKey("news.key"), index=True)
    user: Mapped[int] = mapped_column(ForeignKey("users.key"), index=True)

    def __str__(self) -> str:
        return f"UserLikes(key={self.key}, news={self.news}, user={self.user})"
