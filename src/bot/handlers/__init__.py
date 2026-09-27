from aiogram import Router

from .news import news_command
from .news import news_routers

def routers() -> list[Router]:

    return [
        *news_routers()
    ]