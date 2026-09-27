from aiogram import types

from bot import config
from entity import News, UserLikes, Comment
from repository import Repository
from service import UserService
from .helpers import comments_for_news
from .keyboard import news_list_kb, news_item_kb, comments_kb


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

async def render_comments_page(
    target: types.Message,
    news_id: int,
    page: int,
    news_repo: Repository[News],
    comment_repo: Repository[Comment],
    user_service: UserService,
    edit: bool = False,
) -> None:
    news = news_repo.retrieve(news_id)
    if news is None:
        await target.answer(f"Новость с Id({news_id}) не найдена")
        return

    news_author = await user_service.find_user(news.author)
    if news_author is None:
        await target.answer("У новости невалидный автор")
        return

    comments = comments_for_news(comment_repo, news_id)
    total_comments = len(comments)
    total_pages = (
        max(0, (total_comments - 1) // config.comments_page_size)
        if total_comments > 0
        else 0
    )

    page = min(max(0, page), total_pages)
    start = page * config.comments_page_size
    page_comments = comments[start:start + config.comments_page_size]

    lines = [f"Комментарии к {news.title} | {news_author.name}"]

    for comment in page_comments:
        comment_author = await user_service.find_user(comment.author)
        author_name = comment_author.name if comment_author is not None else "Unknown"

        lines.append(
            f"{author_name}    {comment.creation_date:%Y-%m-%d %H:%M}"
        )
        lines.append(comment.content)
        lines.append("")

    text = "\n".join(lines).rstrip()
    markup = comments_kb(news_id, page, total_pages)

    if edit:
        await target.edit_text(text, reply_markup=markup)
    else:
        await target.answer(text, reply_markup=markup)
