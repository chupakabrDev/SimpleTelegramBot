from dataclasses import dataclass
from datetime import datetime

from src.repository.repository import Keyable


@dataclass
class Comment(Keyable):
    author: int
    news: int
    creation_date: datetime
    content: str

    def __str__(self) -> str:
        return (
            f"Comment(key={self.key}, author={self.author}, news={self.news}, "
            f"created={self.creation_date:%Y-%m-%d %H:%M}, content={self.content!r})"
        )