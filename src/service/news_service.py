from datetime import datetime

from entity import Comment, News, User, UserLikes
from repository import Repository


class NewsService:

    def __init__(self, likes_repo: Repository[UserLikes], comments_repo: Repository[Comment]):
        self.likes_repo = likes_repo
        self.comments_repo = comments_repo

    def like_news(self, news: News, user: User) -> bool:
        user_likes = self.likes_repo.retrieve(news.key)
        if not user_likes:
            user_likes = UserLikes(news)
            self.likes_repo.update_or_create(user_likes)

        if user_likes.like(user):
            self.likes_repo.update_or_create(user_likes)
            return True

        return False

    def unlike_news(self, news: News, user: User) -> bool:
        user_likes = self.likes_repo.retrieve(news.key)
        if user_likes:
            return user_likes.unlike(user)

        return False

    def comment_news(self, news: News, user: User, content: str) -> Comment:
        comment = Comment(user.key, news.key, datetime.now(), content)
        self.comments_repo.update_or_create(comment)
        return comment