from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from entity import News, UserLikes
from repository import Repository
from .callback import NewsViewCallbackData, NewsPaginationCallbackData, NewsLikeCallbackData, NewsCommentCallbackData, \
    CommentsPaginationCallbackData, CreateCommentCallbackData


def news_list_kb(
    news: list[News],
    likes_repo: Repository[UserLikes],
    page: int,
    total_pages: int,
) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for item in news:
        likes = likes_repo.count_filtered(news=item.key)
        builder.add(types.InlineKeyboardButton(
            text=f"title: {item.title} | likes: {likes}",
            callback_data=NewsViewCallbackData(news_id=item.key).pack(),
        ))

    prev_page = max(0, page - 1)
    next_page = min(total_pages - 1, page + 1)

    builder.add(types.InlineKeyboardButton(
        text="<-",
        callback_data=NewsPaginationCallbackData(curr_page=page, new_page=prev_page).pack(),
    ))
    builder.add(types.InlineKeyboardButton(
        text="->",
        callback_data=NewsPaginationCallbackData(curr_page=page, new_page=next_page).pack(),
    ))

    builder.adjust(*([1] * len(news)), 2)
    return builder.as_markup()


def news_item_kb(news_id: int, user_id: int, likes_repo: Repository[UserLikes]) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    likes = likes_repo.count_filtered(news=news_id)
    style = "primary"
    if likes_repo.exists_by(UserLikes.user, user_id):
        style = "success"

    builder.add(types.InlineKeyboardButton(
        text=f"👍 {likes}",
        callback_data=NewsLikeCallbackData(news_id=news_id).pack(),
        style=style
    ))
    builder.add(types.InlineKeyboardButton(
        text=f"💬 Комментировать",
        callback_data=CreateCommentCallbackData(news_id=news_id).pack()
    ))
    builder.add(types.InlineKeyboardButton(
        text="🗪 Комментарии",
        callback_data=NewsCommentCallbackData(news_id=news_id).pack(),
    ))
    builder.adjust(2)
    return builder.as_markup()

def comments_kb(
    news_id: int,
    page: int,
    total_pages: int,
) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    prev_page = max(0, page - 1)
    next_page = min(total_pages - 1, page + 1)

    builder.add(types.InlineKeyboardButton(
        text="<-",
        callback_data=CommentsPaginationCallbackData(
            news_id=news_id,
            curr_page=page,
            new_page=prev_page,
        ).pack(),
    ))
    builder.add(types.InlineKeyboardButton(
        text="->",
        callback_data=CommentsPaginationCallbackData(
            news_id=news_id,
            curr_page=page,
            new_page=next_page,
        ).pack(),
    ))

    builder.adjust(2)
    return builder.as_markup()