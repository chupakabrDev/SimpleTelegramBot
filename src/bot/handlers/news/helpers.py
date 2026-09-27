from entity import UserLikes
from repository import Repository


def likes_count(likes_repo: Repository[UserLikes], news_id: int) -> int:
    likes = likes_repo.retrieve(news_id)
    return likes.count if likes is not None else 0