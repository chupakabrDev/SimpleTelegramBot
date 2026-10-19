import asyncio

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from bot.handlers.news.fsm import CommentCreateFSM
from entity import UserLikes, Comment
from repository import Repository


def likes_count(likes_repo: Repository[UserLikes], news_id: int) -> int:
    likes = likes_repo.retrieve(news_id)
    return likes.count if likes is not None else 0

def comments_for_news(
    comment_repo: Repository[Comment],
    news_id: int,
) -> list[Comment]:
    all_comments = comment_repo.query(0, comment_repo.count())
    return sorted(
        (comment for comment in all_comments if comment.news == news_id),
        key=lambda comment: comment.creation_date,
    )

async def clear_state_after_timeout(bot: Bot, chat_id: int, state: FSMContext, expected_state: State, timeout: int = 60):
    await asyncio.sleep(timeout)

    current_state = await state.get_state()
    if current_state == expected_state.state:
        await state.clear()
        await bot.send_message(chat_id=chat_id, text="Время ожидания для написания истекло, попробуйте снова")
