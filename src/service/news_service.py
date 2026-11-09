from datetime import datetime

from entity import Comment, News, User, UserLikes
from repository import Repository


class NewsService:

    def __init__(self, likes_repo: Repository[UserLikes], comment_repo: Repository[Comment], news_repo: Repository[News]) -> None:
        self.likes_repo = likes_repo
        self.comment_repo = comment_repo
        self.news_repo = news_repo

    def toggle_like(self, news: int, user: User) -> bool:
        hasLike = self.likes_repo.exists_by(UserLikes.user, user.key)

        if hasLike:
            self.likes_repo.delete_by(UserLikes.user, user.key)
            return False

        obj = UserLikes(news=news, user=user.key)
        self.likes_repo.update_or_create(obj)

        return True

    def comment_news(self, news: int, user: User, content: str) -> Comment:
        comment = Comment(user.key, news, datetime.now(), content)
        self.comment_repo.update_or_create(comment)
        return comment

    def write_news(self, user: User, title: str, content: str) -> News:
        news = News(user.key, datetime.now(), title, content)
        self.news_repo.update_or_create(news)
        return news