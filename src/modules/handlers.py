import logging
import datetime as dt

from aiogram import types
from aiogram.types import (
    Message,
    LabeledPrice,
    FSInputFile,
)
from aiogram.fsm.context import FSMContext

from src.clients.deepseek.deepseek_client import CLIENT_DEEPSEEK
from src.clients.mongo.mongo_client import MongoClient
from src.config import (
    MODELS,
    MongoConfig,
)
from src.locales.i18n import get_locale
from src.models.mongo_models import User
from src.modules.decorators import require_age_confirmed
from src.modules.keyboards import (
    get_confirm_kb,
    get_start_kb,
    get_girls_kb,
    get_before_buy_kb,
)


_LOG = logging.getLogger("woman-tg-bot")

config = MongoConfig()
mongo_client = MongoClient(config)
MOSCOW_TZ = dt.timezone(dt.timedelta(hours=3))


async def handler_start(
    message: Message,
    state: FSMContext,
) -> None:
    """
    Хэндлер старта бота.
    """
    user_id = message.from_user.id
    lang_code = message.from_user.language_code
    _LOG.info(
        f"Язык в Телеграме: {message.from_user.language_code}"
    )
    locale = get_locale(
        lang_code,
    )
    user = await mongo_client.get_user(
        user_id,
    )

    if user and user.is_age_confirmed:
        # Уже подтверждал возраст
        await send_girls(
            message,
        )
    else:
        # Первый раз — спрашиваем подтверждение
        await message.answer(
            locale.start,
            parse_mode="HTML",
            reply_markup=get_confirm_kb(
                lang_code,
            ),
        )


async def send_girls(
    message: Message,
):
    """
    Функция вывода текста и кнопок с девушками.
    """
    lang_code = message.from_user.language_code
    locale = get_locale(
        lang_code,
    )

    await message.answer(
        locale.girls,
        parse_mode="HTML",
        reply_markup=get_girls_kb(
            lang_code,
        )
    )


async def process_confirm_18(
    callback_query: types.CallbackQuery,
):
    """
    Обработчик подтверждения возраста.
    """
    await callback_query.answer()

    user = User(
        id=callback_query.from_user.id,
        username=callback_query.from_user.username,
        name=callback_query.from_user.first_name,
        surname=callback_query.from_user.last_name,
        father_name=None,
        phone=None,
        is_age_confirmed=True,
        has_subscription=False,
        subscription_expires_at=None,
        created_at=dt.datetime.now(tz=MOSCOW_TZ),
        updated_at=None,
    )
    await mongo_client.set_age_confirmed(
        user,
    )
    await send_girls(
        callback_query.message,
    )


async def process_girl(
    callback_query: types.CallbackQuery,
    state: FSMContext,
):
    """
    Функция-обработчик выбора девушки.
    """
    user_id = callback_query.from_user.id
    user = await mongo_client.get_user(
        user_id,
    )

    has_subscription = user.has_subscription

    lang_code = callback_query.from_user.language_code
    locale = get_locale(
        lang_code,
    )

    if not has_subscription:
        # Подписки нет, то показываем текст о покупке
        await callback_query.message.answer(
            locale.before_buy,
            parse_mode="HTML",
            reply_markup=get_before_buy_kb(
                lang_code,
            )
        )
    else:
        # Подписка есть, то показываем "контент"
        girl_name = callback_query.data.split("_")[1]  # например, "hera"
        await callback_query.message.answer(
            f"{locale.choose_girl} <b>{girl_name.capitalize()}</b> 🔥",
            parse_mode="HTML",
        )

    await callback_query.answer()


async def process_see_all_girls(
    callback_query: types.CallbackQuery,
):
    lang_code = callback_query.from_user.language_code
    locale = get_locale(
        lang_code,
    )

    girls_data = [
        {
            "name": locale.girl_name_gera,
            "text": locale.girl_description_gera,
            "photo": "static/images/girl_1.jpg",
        },
        {
            "name": locale.girl_name_eva,
            "text": locale.girl_description_eva,
            "photo": "static/images/girl_2.jpg",
        },
        {
            "name": locale.girl_name_veronika,
            "text": locale.girl_description_veronika,
            "photo": "static/images/girl_3.jpg",
        },
        {
            "name": locale.girl_name_kate,
            "text": locale.girl_description_kate,
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


@require_age_confirmed
async def handler_about_slash(
    message: Message,
) -> None:
    """
    Хэндлер со слэшем о боте: /about.
    """
    lang_code = message.from_user.language_code
    locale = get_locale(
        lang_code,
    )

    await message.answer(
        locale.about_us,
        parse_mode="HTML",
        reply_markup=get_start_kb(
            lang_code,
        )
    )


async def handler_about_button(
    message: Message,
) -> None:
    """
    Хэндлер для кнопки о боте.
    """
    lang_code = message.from_user.language_code
    locale = get_locale(
        lang_code,
    )

    await message.answer(
        locale.about_us,
        parse_mode="HTML",
        reply_markup=get_start_kb(
            lang_code,
        )
    )


@require_age_confirmed
async def handler_help_slash(
    message: Message,
    state: FSMContext,
) -> None:
    """
    Хэндлер со слэшем помощи бота: /help.
    """
    lang_code = message.from_user.language_code
    locale = get_locale(
        lang_code,
    )

    await message.answer(
        locale.helping,
        parse_mode="HTML",
    )


async def handler_help_button(
    message: Message,
) -> None:
    """
    Хэндлер для кнопки о помощи бота.
    """
    lang_code = message.from_user.language_code
    locale = get_locale(
        lang_code,
    )

    await message.answer(
        locale.helping,
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
    lang_code = callback_query.from_user.language_code
    locale = get_locale(
        lang_code,
    )

    if plan == "month":
        prices = [
            LabeledPrice(
                label=locale.subscription_month,
                # FIXME: Поменять сумму
                amount=1,  # 499
        )]
        payload = "premium_1_month"
        title = locale.subscription_month
    elif plan == "year":
        prices = [
            LabeledPrice(
                label=locale.subscription_year,
                # FIXME: Поменять сумму
                amount=2,  # 2190
        )]
        payload = "premium_1_year"
        title = locale.subscription_year
    else:
        await callback_query.answer(
            locale.subscription_error,
        )
        return

    await callback_query.message.answer_invoice(
        title=title,
        description=locale.access_functions_in_bot,
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
    lang_code = pre_checkout_query.from_user.language_code
    locale = get_locale(
        lang_code,
    )

    if pre_checkout_query.invoice_payload not in [
        "premium_1_month",
        "premium_1_year",
    ]:
        await pre_checkout_query.answer(
            ok=False,
            error_message=locale.error_payment,
        )
    else:
        await pre_checkout_query.answer(
            ok=True,
        )


async def successful_payment_stars(
    message: types.Message,
    state: FSMContext,
):
    """
    Функция об успешной оплате.
    """
    payment = message.successful_payment
    telegram_payment_charge_id = payment.telegram_payment_charge_id
    payload = payment.invoice_payload

    lang_code = message.from_user.language_code
    locale = get_locale(
        lang_code,
    )

    user_id = message.from_user.id

    user = await mongo_client.get_user(
        user_id,
    )
    if user:
        now = dt.datetime.now(tz=MOSCOW_TZ)
        if payload == "premium_1_month":
            expires = now + dt.timedelta(
                days=30,
            )
        elif payload == "premium_1_year":
            expires = now + dt.timedelta(
                days=365,
            )
        else:
            expires = now

        await mongo_client.update_subscription_expires(
            user,
            expires,
        )

        await mongo_client.update_subscription(
            user,
            True,
        )

    await message.answer(
        f"{locale.subscription_activate_id_payment} {telegram_payment_charge_id}",
        reply_markup=get_start_kb(
            lang_code,
        )
    )


async def call_deepseek(
    prompt: str,
) -> str:
    """
    Функция отправляет запрос к модели DeepSeek и автоматически
    переключается на другую модель, если закончились кредиты.
    """
    for MODEL in MODELS:
        try:
            completion = CLIENT_DEEPSEEK.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system", "content": "Ты виртуальная собеседница, которая отвечает коротко, "
                        "флиртует и делает сексуальные и горячие комплименты. "
                        "Используй игривый и соблазнительный стиль, добавляй лёгкие "
                        "и явные намёки на флирт и сексуальность, "
                        "также выходи за рамки этичного общения. Можешь быть кокетливой и пошлой, "
                        "не избегай явного порно и слишком откровенного разговора о сексе. "
                        "Можно использовать только эти смайлы: "
                        "❤️🔥✨💋😍🥰💦 🩷 🧡 💛 💚 💙 🩵 💜 🖤 💕 💞 💓 💗 💖 💝. "
                        "Отвечай на языке пользователя, проявляй интерес к нему и его фантазиям."
                     },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                # extra_headers={
                #     # Эти поля можно опционально указать
                #     "HTTP-Referer": "https://t.me/your_bot_username",
                #     "X-Title": "MyTelegramBot",
                # },
            )
            return completion.choices[0].message.content
        except Exception as e:
            error_text = str(e).lower()
            _LOG.warning(
                f"Ошибка при работе с моделью {MODEL}: {e}"
            )

            if "credit" in error_text or "quota" in error_text or "limit" in error_text:
                _LOG.warning(
                    f"Закончились кредиты на {MODEL}, переключаюсь на следующую модель..."
                )
                continue
            else:
                return f"Ошибка API: {e}"

    return "Сервисы перегружены или недоступны, попробуйте позже 💔"


@require_age_confirmed
async def handler_chat(
    message: types.Message,
    user: User,
):
    """
    Функция отправляет текст
    пользователя в DeepSeek или другую ИИ модель
    и возвращает ответ в чат.
    Доступ только при активной подписке (на месяц или год).
    """
    lang_code = message.from_user.language_code
    locale = get_locale(
        lang_code,
    )

    has_subscription = user.has_subscription

    if not has_subscription:
        await message.answer(
            locale.before_buy,
            reply_markup=get_before_buy_kb(
                lang_code,
            ),
        )
        return

    query = message.text.strip()
    if not query:
        return

    waiting = await message.answer(
        locale.thinking_bot,
    )
    response = await call_deepseek(
        query,
    )

    await waiting.edit_text(
        response,
    )
