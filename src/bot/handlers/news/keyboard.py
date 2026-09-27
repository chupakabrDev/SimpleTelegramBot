from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from entity import News, UserLikes
from repository import Repository
from .callback import NewsCallbackData, PaginationCallbackData
from .helpers import likes_count


def news_list_kb(
    news: list[News],
    likes_repo: Repository[UserLikes],
    page: int,
    total_pages: int,
) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for item in news:
        likes = likes_count(likes_repo, item.key)
        builder.add(types.InlineKeyboardButton(
            text=f"title: {item.title} | likes: {likes}",
            callback_data=NewsCallbackData.view(news_id=item.key),
        ))

    prev_page = max(0, page - 1)
    next_page = min(total_pages, page + 1)

    builder.add(types.InlineKeyboardButton(
        text="<-",
        callback_data=PaginationCallbackData.news(curr_page=page, new_page=prev_page),
    ))
    builder.add(types.InlineKeyboardButton(
        text="->",
        callback_data=PaginationCallbackData.news(curr_page=page, new_page=next_page),
    ))

    builder.adjust(*([1] * len(news)), 2)
    return builder.as_markup()


def news_item_kb(news_id: int, user_id: int, likes_repo: Repository[UserLikes]) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    likes = likes_repo.retrieve(news_id)
    count = 0
    style = "primary"
    if likes is not None:
        count = likes.count
        if likes.is_liked_by(user_id):
            style = "success"

    builder.add(types.InlineKeyboardButton(
        text=f"👍 {count}",
        callback_data=NewsCallbackData.like(news_id=news_id),
        style=style
    ))
    # builder.add(types.InlineKeyboardButton(
    #     text="💬 Комментарии",
    #     callback_data=NewsCallbackData.comments(news_id=news_id),
    # ))
    # builder.adjust(2)
    return builder.as_markup()