import logging

from aiogram.filters import Command
from aiogram.types import Message

from src import (
    texts,
    keyboards,
)


_LOG = logging.getLogger("woman-tg-bot")


async def register_handlers(
    dp,
):
    @dp.message(
        Command("start"),
    )
    async def handler_start(
        message: Message,
    ) -> None:
        """
        Хэндлер старта бота.
        """
        await message.answer(
            texts.start,
            parse_mode="HTML",
            reply_markup=keyboards.start_kb,
        )

    @dp.message(
        Command("about"),
    )
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

    @dp.message(
        lambda
            message: message.text == "ℹ️ Обо мне",
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
