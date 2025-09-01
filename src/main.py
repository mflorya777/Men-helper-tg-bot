import asyncio
from os import getenv
from dotenv import load_dotenv

from aiogram import (
    Bot,
    Dispatcher,
)
from aiogram.filters import Command
from aiogram.types import Message


load_dotenv()

TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()


@dp.message(Command("start"))
async def handler_start(
    message: Message,
) -> None:
    """
    Хэндлер старта бота.
    """
    await message.answer(
        "Привет! Я бот, сделанный на aiogram."
    )


# Запуск бота
async def main() -> None:
    """
    Функция запуска бота.
    """
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

