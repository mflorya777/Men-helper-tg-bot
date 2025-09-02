import logging

from aiogram import types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext

from src import (
    texts,
    keyboards,
)
from src.fsm_models.fsm_models import AgeConfirm


_LOG = logging.getLogger("woman-tg-bot")



async def handler_start(
    message: Message,
    state: FSMContext,
) -> None:
    """
    Хэндлер старта бота.
    """
    current_state = await state.get_state()
    if current_state == AgeConfirm.confirmed:
        # Уже подтверждал возраст, то сразу кидаем к девушкам
        await send_girls(message)
    else:
        # Первый раз, то спрашиваем подтверждение
        await message.answer(
            texts.start,
            parse_mode="HTML",
            reply_markup=keyboards.confirm_kb,
        )
        await state.set_state(AgeConfirm.not_confirmed)


async def send_girls(
    message: Message,
):
    await message.answer(
        texts.girls,
        parse_mode="HTML",
        reply_markup=keyboards.girls_kb,
    )


async def process_confirm_18(
    callback_query: types.CallbackQuery,
    state: FSMContext,
):
    await state.set_state(AgeConfirm.confirmed)  # сохраняем статус
    await send_girls(callback_query.message)
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
    """
    Функция регистрации всех хэндлеров.
    """
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
