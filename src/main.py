import asyncio
from datetime import datetime, date
from os import getenv
from typing import Any

from aiogram import Bot, Dispatcher

from bot.handlers import news_routers
from entity import News, Comment, User, UserLikes
from repository import InMemoryRepository
from service import UserService
from service.news_service import NewsService

def init_dependencies(bot: Bot) -> dict[str, Any]:
    news_repo = InMemoryRepository[News]()
    comment_repo = InMemoryRepository[Comment]()
    user_repo = InMemoryRepository[User](False)
    likes_repo = InMemoryRepository[UserLikes](False)

    zero_user = User(date.today(), "Bob", "Kovalski")
    zero_user.key = 5741084752
    user_repo.update_or_create(zero_user)

    news_repo.update_or_create(News(5741084752, datetime.now(), "First News", "First news content"))
    news_repo.update_or_create(News(5741084752, datetime.now(), "Interested News", "some news content"))
    news_repo.update_or_create(News(5741084752, datetime.now(), "Original News", "and more news content"))

    comment_repo.update_or_create(Comment(5741084752, 1, datetime.now(), "Best comment content"))
    comment_repo.update_or_create(Comment(5741084752, 1, datetime.now(), "Best comment content 1"))
    comment_repo.update_or_create(Comment(5741084752, 1, datetime.now(), "Best comment content 2"))
    comment_repo.update_or_create(Comment(5741084752, 1, datetime.now(), "Best comment content 3"))

    news_service = NewsService(likes_repo, comment_repo)
    user_service = UserService(bot, user_repo)

    return {
        "news_repo": news_repo,
        "comment_repo": comment_repo,
        "user_repo": user_repo,
        "likes_repo": likes_repo,
        "news_service": news_service,
        "user_service": user_service,
    }

async def main():
    token = getenv("BOT_TOKEN")
    if not token:
        error = "No token provided"
        raise ValueError(error)

    bot = Bot(token=token)

    dp = Dispatcher()
    dp.workflow_data = init_dependencies(bot)
    dp.include_routers(*news_routers())

    print("Starting bot...")
    try:
        await dp.start_polling(bot)
    finally:
        print("Bot stopped")

if __name__ == '__main__':
    asyncio.run(main())