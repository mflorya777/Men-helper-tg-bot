#!/usr/bin/env python

import asyncio
import logging
from os import getenv

from dotenv import load_dotenv

from aiogram import (
    Bot,
    Dispatcher,
)

from src.handlers import register_handlers


_LOG = logging.getLogger("woman-tg-bot")
load_dotenv()

TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()


async def main() -> None:
    """
    Функция запуска бота.
    """
    await register_handlers(dp)
    bot = Bot(
        token=TOKEN,
    )
    _LOG.info(
        "Бот запущен"
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(
        main()
    )

