from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from bot import config
from entity import News
from repository import Repository

router = Router(name="commands_args")


@router.message(Command("news"))
async def cmd_set_timer(
        message: Message,
        command: CommandObject,
        news_repo: Repository[News]
) -> None:

    page = 0
    if command.args is not None:
        try:
            page = max(0, int(command.args))
        except ValueError:
            await message.answer("/news or /news <page: int>")
            return

    start = page * config.news_page_size
    end = start + config.news_page_size # exclusive

    news = news_repo.query(start, end) # недоделано

    await message.answer(

    )