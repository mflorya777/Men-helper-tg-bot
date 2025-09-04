import logging
from functools import partial
from dotenv import load_dotenv

from aiogram import (
    Bot,
    Dispatcher,
    F,
    types,
)
from aiogram.filters import Command

from src.config import TOKEN
from src.modules.handlers import (
    handler_start,
    buy_stars,
    pre_checkout_stars,
    successful_payment_stars,
    process_confirm_18,
    handler_about_slash,
    handler_about_button,
    process_girl,
    handler_help_slash,
    handler_help_button,
    process_see_all_girls,
    handler_dep,
)


_LOG = logging.getLogger("woman-tg-bot")

load_dotenv()
dp = Dispatcher()


async def register_handlers(
    dp: Dispatcher,
):
    """
    Функция регистрации всех хэндлеров.
    """
    dp.callback_query.register(
        partial(
            buy_stars,
            plan="year",
        ),
        F.data == "subscription_year",
    )
    dp.callback_query.register(
        partial(
            buy_stars,
            plan="month",
        ),
        F.data == "subscription_all",
    )
    dp.pre_checkout_query.register(
        pre_checkout_stars,
    )
    dp.message.register(
        successful_payment_stars,
        F.content_type == types.ContentType.SUCCESSFUL_PAYMENT,
    )
    dp.message.register(
        handler_start,
        Command("start"),
    )
    dp.callback_query.register(
        process_confirm_18,
        lambda
            c: c.data == "confirm_18",
    )
    dp.message.register(
        handler_about_slash,
        Command("about"),
    )
    dp.message.register(
        handler_about_button,
        lambda
            message: message.text == "ℹ️ Обо мне",
    )
    dp.message.register(
        handler_help_slash,
        Command("help"),
    )
    dp.message.register(
        handler_help_button,
        lambda
            message: message.text == "❓ Помощь",
    )
    dp.callback_query.register(
        process_girl,
        lambda
            c: c.data.startswith("girl_"),
    )
    dp.callback_query.register(
        process_see_all_girls,
        F.data == "see_all_girls",
    )
    dp.message.register(
        handler_dep,
        Command("dep"),
    )


async def main() -> None:
    """
    Функция запуска бота.
    """
    await register_handlers(
        dp,
    )
    bot = Bot(
        token=TOKEN,
    )
    _LOG.info(
        "Бот запущен"
    )
    await dp.start_polling(
        bot,
    )
