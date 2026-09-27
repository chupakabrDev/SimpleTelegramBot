from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot import config
from entity import News, UserLikes, User
from repository import Repository
from service import NewsService, UserService

router = Router(name="news_command")


class PaginationCallbackData(CallbackData, prefix="news_page"):
    curr_page: int
    new_page: int

class NewsOpenCallbackData(CallbackData, prefix="news_open"):
    news_id: int

class NewsToggleLikeCallbackData(CallbackData, prefix="news_like_toggle"):
    news_id: int

async def render_news_page(
    target: Message,
    page: int,
    news_repo: Repository[News],
    likes_repo: Repository[UserLikes],
    edit: bool = False
) -> None:
    start = page * config.news_page_size
    end = start + config.news_page_size

    news = news_repo.query(start, end)

    builder = InlineKeyboardBuilder()
    for new in news:
        likes = likes_count(likes_repo, new)
        builder.add(types.InlineKeyboardButton(
            text=f"title: {new.title} | likes: {likes}",
            callback_data=NewsOpenCallbackData(news_id=new.key).pack(),
        ))

    total_pages = max(0, (news_repo.count() - 1) // config.news_page_size)
    prev_page = max(0, page - 1)
    next_page = min(total_pages, page + 1)

    builder.add(types.InlineKeyboardButton(
        text="<-",
        callback_data=PaginationCallbackData(curr_page=page, new_page=prev_page).pack(),
    ))
    builder.add(types.InlineKeyboardButton(
        text="->",
        callback_data=PaginationCallbackData(curr_page=page, new_page=next_page).pack(),
    ))

    builder.adjust(*([1] * len(news)), 2)

    if edit:
        await target.edit_text("Выберите новость", reply_markup=builder.as_markup())
    else:
        await target.answer("Выберите новость", reply_markup=builder.as_markup())


@router.message(Command("news"))
async def news_command(
    message: Message,
    command: CommandObject,
    news_repo: Repository[News],
    likes_repo: Repository[UserLikes],
) -> None:
    page = 0
    if command.args is not None:
        try:
            page = max(0, int(command.args))
        except ValueError:
            await message.answer("/news or /news <page: int>")
            return

    await render_news_page(message, page, news_repo, likes_repo)


@router.callback_query(PaginationCallbackData.filter())
async def news_page_callback(
    callback: CallbackQuery,
    callback_data: PaginationCallbackData,
    news_repo: Repository[News],
    likes_repo: Repository[UserLikes],
) -> None:
    if callback_data.curr_page == callback_data.new_page:
        await callback.answer()
        return

    await render_news_page(
        callback.message,
        callback_data.new_page,
        news_repo,
        likes_repo,
        edit=True
    )
    await callback.answer()

async def render_news(
        target: Message,
        news_id: int,
        news_repo: Repository[News],
        likes_repo: Repository[UserLikes],
        user_service: UserService,
        edit: bool = False
) -> None:
    news = news_repo.retrieve(news_id)
    if news is None:
        await target.answer(f"Новость с Id({news_id}) не найдена")
        return

    author = await user_service.find_user(news.author)
    if author is None:
        await target.answer(f"У новости невалидный автор")
        return

    builder = InlineKeyboardBuilder()

    likes = likes_count(likes_repo, news)
    builder.add(types.InlineKeyboardButton(
        text=f"👍 {likes}",
        callback_data=NewsToggleLikeCallbackData(news_id=news_id).pack()
    ))

    msg = f"{news.title}\n{author.name} | {news.creation_date:%Y-%m-%d %H:%M}\n{news.content}"
    buttons = builder.as_markup()
    if edit:
        await target.edit_text(msg, reply_markup=buttons)
    else:
        await target.answer(msg, reply_markup=buttons)

@router.callback_query(NewsOpenCallbackData.filter())
async def news_open_callback(
        callback: CallbackQuery,
        callback_data: NewsOpenCallbackData,
        news_repo: Repository[News],
        likes_repo: Repository[UserLikes],
        user_service: UserService
) -> None:
    await render_news(callback.message, callback_data.news_id, news_repo, likes_repo, user_service)
    await callback.answer()

@router.callback_query(NewsToggleLikeCallbackData.filter())
async def news_toggle_like_callback(
        callback: CallbackQuery,
        callback_data: NewsToggleLikeCallbackData,
        news_service: NewsService,
        likes_repo: Repository[UserLikes],
        news_repo: Repository[News],
        user_service: UserService
) -> None:
    user = await user_service.find_user(callback.from_user.id)
    if user is None:
        await callback.answer("user not found")
    else:
        news_service.toggle_like(callback_data.news_id, user)
        await render_news(callback.message, callback_data.news_id, news_repo, likes_repo, user_service, True)
        await callback.answer()

def likes_count(likes_repo: Repository[UserLikes], news: News) -> int:
    likes = likes_repo.retrieve(news.key)
    return likes.count if likes is not None else 0