from dataclasses import dataclass
from datetime import date

from src.repository.repository import Keyable


@dataclass
class User(Keyable):
    registration_date: date
    name: str
    surname: str

    def __str__(self) -> str:
        return (
            f"User(key={self.key}, {self.name} {self.surname}, "
            f"registered={self.registration_date:%Y-%m-%d})"
        )