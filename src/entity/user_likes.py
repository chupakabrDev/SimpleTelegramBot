from dataclasses import dataclass, field

from repository import Keyable
from . import News, User

@dataclass
class UserLikes(Keyable):
    news: News
    likes: set[int] = field(default_factory=set)

    def __post_init__(self) -> None:
        self._key = self.news.key

    def like(self, user: User) -> bool:
        """Поставить лайк. Возвращает False, если уже стоит."""
        if user.key in self.likes:
            return False
        self.likes.add(user.key)
        return True

    def unlike(self, user: User) -> bool:
        """Убрать лайк. Возвращает False, если лайка не было."""
        if user.key not in self.likes:
            return False
        self.likes.remove(user.key)
        return True

    @property
    def count(self) -> int:
        return len(self.likes)

    def __str__(self) -> str:
        return f"UserLikes(news={self.news.key}, count={self.count})"
