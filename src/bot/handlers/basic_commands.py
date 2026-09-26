from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from bot import config

router = Router(name="commands_args")


@router.message(Command("news"))
async def cmd_set_timer(
        message: Message,
        command: CommandObject
) -> None:

    page = 0
    if command.args is not None:
        try:
            page = max(0, int(command.args))
        except ValueError:
            await message.answer("/news or /news <page: int>")
        return

    start = page * config.news_page_size

    await message.answer(

    )