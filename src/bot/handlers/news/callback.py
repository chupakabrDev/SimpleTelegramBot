from aiogram.filters.callback_data import CallbackData

class NewsViewCallbackData(CallbackData, prefix="view"):
    news_id: int

class NewsLikeCallbackData(CallbackData, prefix="like"):
    news_id: int

class NewsCommentCallbackData(CallbackData, prefix="comment"):
    news_id: int

class NewsPaginationCallbackData(CallbackData, prefix="news_pagination"):
    curr_page: int
    new_page: int

class CommentsPaginationCallbackData(CallbackData, prefix="comments_pagination"):
    curr_page: int
    new_page: int
    news_id: int
