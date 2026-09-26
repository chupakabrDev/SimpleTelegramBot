import asyncio
from os import getenv
from typing import Any

from aiogram import Bot, Dispatcher

from entity import News, Comment, User, UserLikes
from repository import InMemoryRepository
from service.news_service import NewsService

dp = Dispatcher()


def init_dependencies() -> dict[str, Any]:
    news_repo = InMemoryRepository[News]()
    comment_repo = InMemoryRepository[Comment]()
    user_repo = InMemoryRepository[User]()
    likes_repo = InMemoryRepository[UserLikes](False)

    news_service = NewsService(likes_repo, comment_repo)

    return {
        "news_repo": news_repo,
        "comment_repo": comment_repo,
        "user_repo": user_repo,
        "likes_repo": likes_repo,
        "news_service": news_service,
    }

async def main():
    token = getenv("BOT_TOKEN")
    if not token:
        error = "No token provided"
        raise ValueError(error)

    bot = Bot(token=token)
    dp.workflow_data = init_dependencies()

    print("Starting bot...")
    try:
        await dp.start_polling(bot)
    finally:
        print("Bot stopped")

if __name__ == '__main__':
    asyncio.run(main())