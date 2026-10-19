from aiogram.fsm.state import StatesGroup, State


class CommentCreateFSM(StatesGroup):
    waiting_for_comment = State()

class NewsCreateFSM(StatesGroup):
    waiting_for_title = State()
    waiting_for_news = State()