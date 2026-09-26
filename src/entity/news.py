from dataclasses import dataclass
from datetime import datetime

from src.repository.repository import Keyable


@dataclass
class News(Keyable):
    author: int
    creation_date: datetime
    title: str
    content: str

    def __str__(self) -> str:
        return (
            f"News(key={self.key}, author={self.author}, "
            f"created={self.creation_date:%Y-%m-%d %H:%M}, title={self.title!r})"
        )