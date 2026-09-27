from aiogram import Router

from . import news_command, view


def news_routers() -> list[Router]:

    return [
        news_command.router,
        view.router,
    ]
