from enum import Enum

from aiogram import F
from aiogram.filters.callback_data import CallbackData

class NewsCallbackType(Enum):
    VIEW = "view"
    LIKE = "like"

    @property
    def filter(self):
        return NewsCallbackData.filter(F.callback_type == self)

class PaginationCallbackType(Enum):
    NEWS = "news"
    COMMENTS = "comments"

    @property
    def filter(self):
        return PaginationCallbackData.filter(F.callback_type == self)

class PaginationCallbackData(CallbackData, prefix="pagination"):
    callback_type: PaginationCallbackType
    curr_page: int
    new_page: int

    @classmethod
    def of(cls, callback_type: PaginationCallbackType, curr_page: int, new_page: int) -> str:
        return cls(
            callback_type=callback_type,
            curr_page=curr_page,
            new_page=new_page,
        ).pack()

    @classmethod
    def news(cls, curr_page: int, new_page: int) -> str:
        return PaginationCallbackData.of(PaginationCallbackType.NEWS, curr_page, new_page)

    @classmethod
    def comments(cls, curr_page: int, new_page: int) -> str:
        return PaginationCallbackData.of(PaginationCallbackType.COMMENTS, curr_page, new_page)


class NewsCallbackData(CallbackData, prefix="news"):
    callback_type: NewsCallbackType
    news_id: int

    @classmethod
    def of(cls, callback_type: NewsCallbackType, news_id: int) -> str:
        return cls(
            callback_type=callback_type,
            news_id=news_id,
        ).pack()

    @classmethod
    def view(cls, news_id: int) -> str:
        return cls.of(NewsCallbackType.VIEW, news_id)

    @classmethod
    def like(cls, news_id: int) -> str:
        return cls.of(NewsCallbackType.LIKE, news_id)
