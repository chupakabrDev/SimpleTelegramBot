import asyncio

from aiogram import Router, types, Bot, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from entity import News, UserLikes, Comment
from repository import Repository
from service import NewsService, UserService
from .callback import NewsViewCallbackData, NewsLikeCallbackData, NewsCommentCallbackData, \
    CommentsPaginationCallbackData, CreateCommentCallbackData
from .fsm import CommentCreateFSM, NewsCreateFSM
from .helpers import clear_state_after_timeout
from .render import render_news, render_comments_page

router = Router(name="news_view")


@router.callback_query(NewsViewCallbackData.filter())
async def news_open_callback(
    callback: types.CallbackQuery,
    callback_data: NewsViewCallbackData,
    news_repo: Repository[News],
    likes_repo: Repository[UserLikes],
    user_service: UserService,
) -> None:
    await render_news(
        callback.message, callback_data.news_id, callback.from_user.id,
        news_repo, likes_repo, user_service,
    )
    await callback.answer()


@router.callback_query(NewsLikeCallbackData.filter())
async def news_toggle_like_callback(
    callback: types.CallbackQuery,
    callback_data: NewsLikeCallbackData,
    news_service: NewsService,
    likes_repo: Repository[UserLikes],
    news_repo: Repository[News],
    user_service: UserService,
) -> None:
    user = await user_service.find_user(callback.from_user.id)
    if user is None:
        await callback.answer("Вы как пользователь отсутствуете в базе")
        return

    news_service.toggle_like(callback_data.news_id, user)
    await render_news(
        callback.message, callback_data.news_id, user.key,
        news_repo, likes_repo, user_service,
        edit=True,
    )
    await callback.answer()

@router.callback_query(NewsCommentCallbackData.filter())
async def news_comments_callback(
    callback: types.CallbackQuery,
    callback_data: NewsCommentCallbackData,
    news_repo: Repository[News],
    comment_repo: Repository[Comment],
    user_service: UserService,
) -> None:
    await render_comments_page(
        callback.message,
        callback_data.news_id,
        0,
        news_repo,
        comment_repo,
        user_service,
        edit=False,
    )
    await callback.answer()


@router.callback_query(CommentsPaginationCallbackData.filter())
async def comments_page_callback(
    callback: types.CallbackQuery,
    callback_data: CommentsPaginationCallbackData,
    news_repo: Repository[News],
    comment_repo: Repository[Comment],
    user_service: UserService,
) -> None:
    if callback_data.curr_page != callback_data.new_page:
        await render_comments_page(
            callback.message,
            callback_data.news_id,
            callback_data.new_page,
            news_repo,
            comment_repo,
            user_service,
            edit=True,
        )
    await callback.answer()

@router.callback_query(CreateCommentCallbackData.filter())
async def create_comment_callback(
    callback: types.CallbackQuery,
    callback_data: CreateCommentCallbackData,
    state: FSMContext,
    bot: Bot
) -> None:
    await state.set_state(CommentCreateFSM.waiting_for_comment)
    await state.update_data(news_id=callback_data.news_id)

    asyncio.create_task(clear_state_after_timeout(bot, callback.from_user.id, state, CommentCreateFSM.waiting_for_comment, timeout=300))

    await callback.message.answer("Напишите ваш комментарий:")

    await callback.answer()

@router.message(CommentCreateFSM.waiting_for_comment, F.text)
async def process_create_comment(message: Message, state: FSMContext, news_service: NewsService, user_service: UserService) -> None:
    user = await user_service.find_user(message.from_user.id)
    news_id = await state.get_value("news_id")

    news_service.comment_news(news_id, user, message.text)

    await message.answer(f"Ваш комментарий принят")
    await state.clear()


@router.message(NewsCreateFSM.waiting_for_title, F.text)
async def process_create_comment(message: Message, state: FSMContext) -> None:
    await state.set_state(NewsCreateFSM.waiting_for_news)
    await state.update_data(title=message.text)

    await message.answer(f"Теперь напишите новость")


@router.message(NewsCreateFSM.waiting_for_news, F.text)
async def process_create_comment(message: Message, state: FSMContext, news_service: NewsService, user_service: UserService) -> None:
    title = await state.get_value("title")
    content = message.text
    user = await user_service.find_user(message.from_user.id)

    news_service.write_news(user, title, content)

    await message.answer(f"Новость {title} написана")
    await state.clear()
