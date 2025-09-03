from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from src.locales.i18n import get_locale


def get_start_kb(
    lang_code: str,
) -> ReplyKeyboardMarkup:
    locale = get_locale(
        lang_code,
    )
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=locale.kb_help,
                ),
                KeyboardButton(
                    text=locale.kb_about,
                ),
            ],
        ],
        resize_keyboard=True,
    )


def get_confirm_kb(
    lang_code: str,
) -> InlineKeyboardMarkup:
    locale = get_locale(
        lang_code,
    )
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=locale.kb_confirm_18,
                    callback_data="confirm_18",
                ),
            ]
        ]
    )


def get_girls_kb(
    lang_code: str,
) -> InlineKeyboardMarkup:
    locale = get_locale(
        lang_code,
    )
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"💃 {locale.girl_name_gera}",
                    callback_data="girl_hera",
                ),
                InlineKeyboardButton(
                    text=f"👠 {locale.girl_name_eva}",
                    callback_data="girl_eva",
                ),
                InlineKeyboardButton(
                    text=f"👸🏻 {locale.girl_name_veronika}",
                    callback_data="girl_veronika",
                ),
                InlineKeyboardButton(
                    text=f"👩🏻‍🦰 {locale.girl_name_kate}",
                    callback_data="girl_kate",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"✨ {locale.kb_see_all}",
                    callback_data="see_all_girls",
                )
            ],
        ],
    )


def get_before_buy_kb(
    lang_code: str,
) -> InlineKeyboardMarkup:
    locale = get_locale(
        lang_code,
    )
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"🔥 {locale.kb_subscribtion_year}",
                    callback_data="subscription_year",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"🔥 {locale.kb_subscribtion}",
                    callback_data="subscription_all",
                ),
            ],
            # Если решишь добавить бесплатную подписку
            # [
            #     InlineKeyboardButton(
            #         text="🤝 Получить подписку бесплатно",
            #         callback_data="subscription_free",
            #     ),
            # ],
        ],
    )
