import asyncio
from datetime import datetime, date
from os import getenv
from typing import Any

from aiogram import Bot, Dispatcher

from bot.handlers import get_routers
from entity import News, Comment, User, UserLikes
from repository import InMemoryRepository
from service.news_service import NewsService

def init_dependencies() -> dict[str, Any]:
    news_repo = InMemoryRepository[News]()
    comment_repo = InMemoryRepository[Comment]()
    user_repo = InMemoryRepository[User]()
    likes_repo = InMemoryRepository[UserLikes](False)

    user_repo.update_or_create(User(date.today(), "Bob", "Kovalski"))

    news_repo.update_or_create(News(0, datetime.now(), "First News", "First news content"))
    news_repo.update_or_create(News(0, datetime.now(), "Interested News", "some news content"))
    news_repo.update_or_create(News(0, datetime.now(), "Original News", "and more news content"))

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

    dp = Dispatcher()
    dp.workflow_data = init_dependencies()
    dp.include_routers(*get_routers())

    print("Starting bot...")
    try:
        await dp.start_polling(bot)
    finally:
        print("Bot stopped")

if __name__ == '__main__':
    asyncio.run(main())