from aiogram import Router, types

from entity import News, UserLikes
from repository import Repository
from service import NewsService, UserService
from .callback import NewsViewCallbackData, NewsLikeCallbackData
from .render import render_news

router = Router(name="news_view")


@router.callback_query(NewsViewCallbackData.filter())
async def news_open_callback(
    callback: types.CallbackQuery,
    callback_data: NewsViewCallbackData,
    news_repo: Repository[News],
    likes_repo: Repository[UserLikes],
    user_service: UserService,
) -> None:
    await render_news(
        callback.message, callback_data.news_id, callback.from_user.id,
        news_repo, likes_repo, user_service,
    )
    await callback.answer()


@router.callback_query(NewsLikeCallbackData.filter())
async def news_toggle_like_callback(
    callback: types.CallbackQuery,
    callback_data: NewsLikeCallbackData,
    news_service: NewsService,
    likes_repo: Repository[UserLikes],
    news_repo: Repository[News],
    user_service: UserService,
) -> None:
    user = await user_service.find_user(callback.from_user.id)
    if user is None:
        await callback.answer("Вы как пользователь отсутствуете в базе")
        return

    news_service.toggle_like(callback_data.news_id, user)
    await render_news(
        callback.message, callback_data.news_id, user.key,
        news_repo, likes_repo, user_service,
        edit=True,
    )
    await callback.answer()