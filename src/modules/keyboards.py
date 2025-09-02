from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="❓ Помощь"),
            KeyboardButton(text="ℹ️ Обо мне"),
        ],
    ],
    resize_keyboard=True,
)

confirm_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔞 Я старше 18 лет, давай начнем",
                    callback_data="confirm_18"
                ),
            ]
        ]
    )

girls_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="💃 Гера",
                callback_data="girl_hera",
            ),
            InlineKeyboardButton(
                text="👠 Ева",
                callback_data="girl_eva",
            ),
            InlineKeyboardButton(
                text="👸🏻 Вероника",
                callback_data="girl_veronika",
            ),
            InlineKeyboardButton(
                text="👩🏻‍🦰 Кейт",
                callback_data="girl_kate",
            ),
        ],
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
