from aiogram import Router

from .news import news_command
from .news import news_routers
from .start import start_command
from .start import start_routers


def routers() -> list[Router]:

    return [
        *news_routers(),
        *start_routers()
    ]