import logging

from aiogram import types
from aiogram.types import (
    Message,
    LabeledPrice,
)
from aiogram.fsm.context import FSMContext

from src.modules import (
    keyboards,
    texts,
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


async def buy_stars(
    callback_query: types.CallbackQuery,
    plan: str = "month",
):
    """
    Функция отправки счета на Telegram Stars.
    plan: 'month' или 'year'.
    """
    if plan == "month":
        prices = [LabeledPrice(
            label="Подписка Premium на месяц",
            # FIXME: Поменять сумму
            amount=1,  # 499
        )]
        payload = "premium_1_month"
        title = "Подписка Premium (Месяц)"
    elif plan == "year":
        prices = [LabeledPrice(
            label="Подписка Premium на год",
            # FIXME: Поменять сумму
            amount=2,  # 4190
        )]
        payload = "premium_1_year"
        title = "Подписка Premium (Год)"
    else:
        await callback_query.answer("Неверный тип подписки!")
        return

    await callback_query.message.answer_invoice(
        title=title,
        description="Доступ ко всем функциям бота",
        payload=payload,
        provider_token="",
        currency="XTR",
        prices=prices,
        start_parameter=payload,
    )
    await callback_query.answer()


async def pre_checkout_stars(
    pre_checkout_query: types.PreCheckoutQuery,
):
    """
    Функция о предварительном подтверждении оплаты.
    """
    if pre_checkout_query.invoice_payload != "premium_1_month":
        await pre_checkout_query.answer(
            ok=False,
            error_message="Что-то пошло не так...",
        )
    else:
        await pre_checkout_query.answer(
            ok=True,
        )


# FIXME: Здесь уже вместо start_kb добавить продолжение-общение с нейронкой
# TODO: Добавить сохранение уровня аккаунт (премиум или нет) через базу
async def successful_payment_stars(
    message: types.Message,
    state: FSMContext,
):
    """
    Функция об успешной оплате.
    """
    payment = message.successful_payment
    telegram_payment_charge_id = payment.telegram_payment_charge_id

    # Сохраняем флаг подписки в FSM
    await state.update_data(
        has_subscription=True,
    )

    # FIXME: Здесь уже вместо start_kb добавить продолжение-общение с нейронкой
    await message.answer(
        f"✅ Подписка успешно оформлена! ID платежа: {telegram_payment_charge_id}",
        reply_markup=keyboards.start_kb,
    )
