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
