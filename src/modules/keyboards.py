from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from src.locales import texts_ru


start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=texts_ru.kb_help),
            KeyboardButton(text=texts_ru.kb_about),
        ],
    ],
    resize_keyboard=True,
)

confirm_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=texts_ru.kb_confirm_18,
                    callback_data="confirm_18"
                ),
            ]
        ]
    )

girls_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"💃 {texts_ru.girl_name_gera}",
                callback_data="girl_hera",
            ),
            InlineKeyboardButton(
                text=f"👠 {texts_ru.girl_name_eva}",
                callback_data="girl_eva",
            ),
            InlineKeyboardButton(
                text=f"👸🏻 {texts_ru.girl_name_veronika}",
                callback_data="girl_veronika",
            ),
            InlineKeyboardButton(
                text=f"👩🏻‍🦰{texts_ru.girl_name_kate}",
                callback_data="girl_kate",
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"✨ {texts_ru.kb_see_all}",
                callback_data="see_all_girls",
            )
        ]
    ],
    resize_keyboard=True,
)

before_buy_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔥 Оформить подписку на год (Скидка 30%!)",
                callback_data="subscription_year",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔥 Оформить подписку",
                callback_data="subscription_all",
            ),
        ],
        # [
        #     InlineKeyboardButton(
        #         text="🤝 Получить подписку бесплатно",
        #         callback_data="subscription_free",
        #     ),
        # ],
    ],
    resize_keyboard=False,
)
