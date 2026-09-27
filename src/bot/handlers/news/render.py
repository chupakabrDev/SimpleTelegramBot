from aiogram import types

from bot import config
from entity import News, UserLikes
from repository import Repository
from service import UserService
from .keyboard import news_list_kb, news_item_kb


async def render_news_page(
    target: types.Message,
    page: int,
    news_repo: Repository[News],
    likes_repo: Repository[UserLikes],
    edit: bool = False,
) -> None:
    start = page * config.news_page_size
    news = news_repo.query(start, start + config.news_page_size)

    total_pages = max(0, (news_repo.count() - 1) // config.news_page_size)
    markup = news_list_kb(news, likes_repo, page, total_pages)

    text = "Выберите новость"
    if edit:
        await target.edit_text(text, reply_markup=markup)
    else:
        await target.answer(text, reply_markup=markup)


async def render_news(
    target: types.Message,
    news_id: int,
    user_id,
    news_repo: Repository[News],
    likes_repo: Repository[UserLikes],
    user_service: UserService,
    edit: bool = False
) -> None:
    news = news_repo.retrieve(news_id)
    if news is None:
        await target.answer(f"Новость с Id({news_id}) не найдена")
        return

    author = await user_service.find_user(news.author)
    if author is None:
        await target.answer("У новости невалидный автор")
        return

    markup = news_item_kb(news.key, user_id, likes_repo)
    text = f"\t{news.title}\n{author.name} | {news.creation_date:%Y-%m-%d %H:%M}\n{news.content}"

    if edit:
        await target.edit_text(text, reply_markup=markup)
    else:
        await target.answer(text, reply_markup=markup)