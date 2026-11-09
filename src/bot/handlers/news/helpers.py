import asyncio

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State


async def clear_state_after_timeout(bot: Bot, chat_id: int, state: FSMContext, expected_state: State, timeout: int = 60):
    await asyncio.sleep(timeout)

    current_state = await state.get_state()
    if current_state == expected_state.state:
        await state.clear()
        await bot.send_message(chat_id=chat_id, text="Время ожидания для написания истекло, попробуйте снова")
