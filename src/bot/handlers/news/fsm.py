from aiogram.fsm.state import StatesGroup, State


class CommentCreateFSM(StatesGroup):
    waiting_for_comment = State()
