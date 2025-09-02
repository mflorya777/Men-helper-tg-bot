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


# FIXME: Вместо флага из модели FSM сделать через БД Mongo
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
    """
    Функция вывода текста и кнопок с девушками.
    """
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


async def process_girl(
    callback_query: types.CallbackQuery,
    state: FSMContext,
):
    # Достаём из FSM флаг подписки
    data = await state.get_data()
    has_subscription = data.get("has_subscription", False)

    if not has_subscription:
        # Подписки нет, то показываем текст о покупке
        await callback_query.message.answer(
            texts.before_buy,
            parse_mode="HTML",
            reply_markup=keyboards.before_buy_kb,
        )
    else:
        # Подписка есть, то показываем "контент"
        girl_name = callback_query.data.split("_")[1]  # например, "hera"
        await callback_query.message.answer(
            f"Ты выбрал девушку: <b>{girl_name.capitalize()}</b> 😉",
            parse_mode="HTML",
        )

    await callback_query.answer()


# TODO: Сделать обработку покупки через звезды в Телеграм
# Обработка покупки (пока заглушка)
async def process_subscription_year(
    callback_query: types.CallbackQuery,
    state: FSMContext,
):
    # Сохраняем флаг подписки
    await state.update_data(has_subscription=True)
    await callback_query.message.answer("✅ Подписка на год активирована!")
    await callback_query.answer()


async def process_subscription_all(
    callback_query: types.CallbackQuery,
    state: FSMContext,
):
    await state.update_data(has_subscription=True)
    await callback_query.message.answer("✅ Подписка активирована!")
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
    dp.callback_query.register(
        process_girl,
        lambda
            c: c.data.startswith("girl_"),
    )
    dp.callback_query.register(
        process_subscription_year,
        lambda
            c: c.data == "subscription_year",
    )
    dp.callback_query.register(
        process_subscription_all,
        lambda
            c: c.data == "subscription_all",
    )
