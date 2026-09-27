from aiogram import Router, types
from aiogram.filters import Command, CommandObject

from entity import News, UserLikes
from repository import Repository
from .callback import PaginationCallbackType, PaginationCallbackData
from .render import render_news_page

router = Router(name="news")


@router.message(Command("news"))
async def news_command(
    message: types.Message,
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


@router.callback_query(PaginationCallbackType.NEWS.filter)
async def news_page_callback(
    callback: types.CallbackQuery,
    callback_data: PaginationCallbackData,
    news_repo: Repository[News],
    likes_repo: Repository[UserLikes],
) -> None:
    if callback_data.curr_page != callback_data.new_page:
        await render_news_page(
            callback.message,
            callback_data.new_page,
            news_repo,
            likes_repo,
            edit=True,
        )
    await callback.answer()