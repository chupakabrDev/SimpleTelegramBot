from aiogram import Router

from . import start_command


def start_routers() -> list[Router]:

    return [
        start_command.router
    ]
