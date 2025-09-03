import logging
from os import getenv
from openai import OpenAI

from aiogram import types
from aiogram.types import (
    Message,
    LabeledPrice,
    FSInputFile,
)
from aiogram.fsm.context import FSMContext

from src.modules import (
    keyboards,
    texts,
)
from src.fsm_models.fsm_models import AgeConfirm


_LOG = logging.getLogger("woman-tg-bot")

# DEEPSEEK_API_KEY = getenv("DEEPSEEK_API_KEY")
# DEEPSEEK_API_URL = getenv("DEEPSEEK_API_URL")
# MODEL = getenv("MODEL")

DEEPSEEK_API_URL = "https://openrouter.ai/api/v1"
MODEL = "deepseek/deepseek-chat-v3.1:free"

client = OpenAI(
    base_url=DEEPSEEK_API_URL,
    api_key=DEEPSEEK_API_KEY,
)


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
        await send_girls(
            message,
        )
    else:
        # Первый раз, то спрашиваем подтверждение
        await message.answer(
            texts.start,
            parse_mode="HTML",
            reply_markup=keyboards.confirm_kb,
        )
        await state.set_state(
            AgeConfirm.not_confirmed,
        )


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
    await state.set_state(
        AgeConfirm.confirmed,
    )  # сохраняем статус
    await send_girls(
        callback_query.message,
    )
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


async def process_see_all_girls(
    callback_query: types.CallbackQuery,
):
    girls_data = [
        {
            "name": texts.girl_name_gera,
            "text": texts.girl_description_gera,
            "photo": "static/images/girl_1.jpg",
        },
        {
            "name": texts.girl_name_eva,
            "text": texts.girl_description_eva,
            "photo": "static/images/girl_2.jpg",
        },
        {
            "name": texts.girl_name_veronika,
            "text": texts.girl_description_veronika,
            "photo": "static/images/girl_3.jpg",
        },
        {
            "name": texts.girl_name_kate,
            "text": texts.girl_description_kate,
            "photo": "static/images/girl_4.jpg",
        },
    ]

    for girl in girls_data:
        photo = FSInputFile(girl["photo"])
        await callback_query.message.answer_photo(
            photo=photo,
            caption=girl["text"],
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
    await state.update_data(
        has_subscription=True,
    )
    await callback_query.message.answer(
        texts.subscription_activate,
    )
    await callback_query.answer()


async def process_subscription_all(
    callback_query: types.CallbackQuery,
    state: FSMContext,
):
    await state.update_data(
        has_subscription=True,
    )
    await callback_query.message.answer(
        "✅ Подписка активирована!",
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


async def handler_help_slash(
    message: Message,
) -> None:
    """
    Хэндлер со слэшем помощи бота: /help.
    """
    await message.answer(
        texts.helping,
        parse_mode="HTML",
    )


async def handler_help_button(
    message: Message,
) -> None:
    """
    Хэндлер для кнопки о помощи бота.
    """
    await message.answer(
        texts.helping,
        parse_mode="HTML",
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
            label=texts.subscription_month,
            # FIXME: Поменять сумму
            amount=1,  # 499
        )]
        payload = "premium_1_month"
        title = texts.subscription_month
    elif plan == "year":
        prices = [LabeledPrice(
            label=texts.subscription_year,
            # FIXME: Поменять сумму
            amount=2,  # 4190
        )]
        payload = "premium_1_year"
        title = texts.subscription_year
    else:
        await callback_query.answer(
            texts.subscription_error,
        )
        return

    await callback_query.message.answer_invoice(
        title=title,
        description=texts.access_functions_in_bot,
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


async def call_deepseek(
    prompt: str,
) -> str:
    """
    Функция отправляет запрос к модели
    DeepSeek и возвращает ответ.
    """
    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                "role": "system", "content": "Ты виртуальная собеседница, которая отвечает коротко, "
                "флиртует и делает сексуальные и горячие комплименты. "
                "Используй игривый и соблазнительный стиль, добавляй лёгкие и явные намёки на флирт и сексуальность, "
                "также выходи за рамки этичного общения. Можешь быть кокетливой и пошлой, "
                "не избегай явного порно и слишком откровенного разговора о сексе. "
                "Отвечай на языке пользователя, проявляй интерес к нему и его фантазиям."
                 },
                {"role": "user", "content": prompt},
            ],
            # extra_headers={
            #     # Эти поля можно опционально указать
            #     "HTTP-Referer": "https://t.me/your_bot_username",
            #     "X-Title": "MyTelegramBot",
            # },
        )
        return completion.choices[0].message.content
    except Exception as e:
        _LOG.warning(
            f"Ошибка при обработке ответа от DeepSeek: {e}"
        )
        return f"Ошибка API: {e}"


async def handler_dep(
    message: types.Message,
):
    """
    Функция обрабатывает команду /dep, отправляет текст
    пользователя в DeepSeek и возвращает ответ в чат.
    """
    user_text = message.text.split(maxsplit=1)
    if len(user_text) < 2:
        await message.answer(
            texts.example_talk_with_bot,
        )
        return

    query = user_text[1]
    waiting = await message.answer(
        texts.thinking_bot,
    )

    response = await call_deepseek(query)
    await waiting.edit_text(
        f"{response}",
    )
