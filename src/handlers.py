import logging

from aiogram import types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Dispatcher

from src import (
    texts,
    keyboards,
)


_LOG = logging.getLogger("woman-tg-bot")


async def handler_start(
    message: Message,
) -> None:
    """
    Хэндлер старта бота.
    """
    await message.answer(
        texts.start,
        parse_mode="HTML",
        reply_markup=keyboards.confirm_kb,
    )


# TODO: Поменять текст и добавить нужные кнопки (4 штуки)
async def process_confirm_18(
    callback_query: types.CallbackQuery,
):
    await callback_query.message.answer(
        texts.about_us,
        parse_mode="HTML",
        reply_markup=keyboards.start_kb,
    )
    await callback_query.answer()


async def handler_about_slash(
    message: Message,
) -> None:
    """
    Хэндлер со слэшем о боте: /about.
    """
    await message.answer(
        texts.about_us,
        parse_mode="HTML",
        reply_markup=keyboards.start_kb,
    )


async def handler_about_button(
        message: Message,
) -> None:
    """
    Хэндлер для кнопки о боте.
    """
    await message.answer(
        texts.about_us,
        parse_mode="HTML",
        reply_markup=keyboards.start_kb,
    )


async def register_handlers(
    dp: Dispatcher,
):
    dp.message.register(
        handler_start,
        Command("start"),
    )
    dp.callback_query.register(
        process_confirm_18,
        lambda c: c.data == "confirm_18",
    )
    dp.message.register(
        handler_about_slash,
        Command("about"),
    )
    dp.message.register(
        handler_about_button,
        lambda message: message.text == "ℹ️ Обо мне",
    )
