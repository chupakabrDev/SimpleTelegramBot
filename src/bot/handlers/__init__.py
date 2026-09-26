from aiogram import Router

from . import news_command


def get_routers() -> list[Router]:

    return [
        news_command.router,
    ]