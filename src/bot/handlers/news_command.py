from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot import config
from entity import News, UserLikes
from repository import Repository

router = Router(name="news_command")


class Pagination(CallbackData, prefix="news_page"):
    curr_page: int
    new_page: int


async def render_news_page(
    target: Message,                       # куда отвечать
    page: int,
    news_repo: Repository[News],
    likes_repo: Repository[UserLikes],
    edit: bool = False,                    # редактировать или отправлять новое
) -> None:
    start = page * config.news_page_size
    end = start + config.news_page_size

    news = news_repo.query(start, end)

    builder = InlineKeyboardBuilder()
    for new in news:
        likes = likes_repo.retrieve(new.key)
        like_count = likes.count if likes is not None else 0

        builder.add(types.InlineKeyboardButton(
            text=f"title: {new.title} | likes: {like_count}",
            callback_data=f"news_open_{new.key}",
        ))

    total_pages = max(0, (news_repo.count() - 1) // config.news_page_size)
    prev_page = max(0, page - 1)
    next_page = min(total_pages, page + 1)

    builder.add(types.InlineKeyboardButton(
        text="<-",
        callback_data=Pagination(curr_page=page, new_page=prev_page).pack(),
    ))
    builder.add(types.InlineKeyboardButton(
        text="->",
        callback_data=Pagination(curr_page=page, new_page=next_page).pack(),
    ))

    builder.adjust(*([1] * len(news)), 2)

    if edit:
        await target.edit_text("Выберите новость", reply_markup=builder.as_markup())
    else:
        await target.answer("Выберите новость", reply_markup=builder.as_markup())


@router.message(Command("news"))
async def news_command(
    message: Message,
    command: CommandObject,
    news_repo: Repository[News],
    likes_repo: Repository[UserLikes],
) -> None:
    page = 0
    if command.args is not None:
        try:
            page = max(0, int(command.args))
        except ValueError:
            await message.answer("/news or /news <page: int>")
            return

    await render_news_page(message, page, news_repo, likes_repo)


@router.callback_query(Pagination.filter())
async def news_page_callback(
    callback: CallbackQuery,
    callback_data: Pagination,
    news_repo: Repository[News],
    likes_repo: Repository[UserLikes],
) -> None:
    if callback_data.curr_page == callback_data.new_page:
        await callback.answer()
        return

    await render_news_page(
        callback.message,
        callback_data.new_page,
        news_repo,
        likes_repo,
        edit=True,
    )
    await callback.answer()