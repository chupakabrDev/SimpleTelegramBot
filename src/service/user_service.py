from dataclasses import dataclass
from datetime import datetime

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from entity import User
from repository import Repository

@dataclass
class UserService:
    bot: Bot
    user_repo: Repository[User]

    def find_user(self, id: int) -> User | None:
        user = self.user_repo.retrieve(id)
        if user is None:
            try:
                chat = self.bot.get_chat(id)
                user = User(datetime.now(), chat.first_name, chat.last_name)
                user.key = id
            except TelegramBadRequest as _:
                return None

        return user
