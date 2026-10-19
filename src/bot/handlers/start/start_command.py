from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message):
    builder = ReplyKeyboardBuilder()

    builder.button(text="/news")
    builder.button(text="/write")

    builder.adjust(2)

    await message.answer(
        "Выберите действие на клавиатуре",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )
