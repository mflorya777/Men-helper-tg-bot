#!/usr/bin/env python

import asyncio
import logging
from os import getenv

from dotenv import load_dotenv

from aiogram import (
    Bot,
    Dispatcher,
)
from aiogram.filters import Command
from aiogram.types import Message

from src import (
    texts,
    keyboards,
)


_LOG = logging.getLogger("woman-tg-bot")
load_dotenv()

TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()


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
    lambda message: message.text == "ℹ️ Обо мне",
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


async def main() -> None:
    """
    Функция запуска бота.
    """
    bot = Bot(token=TOKEN)
    _LOG.info("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

