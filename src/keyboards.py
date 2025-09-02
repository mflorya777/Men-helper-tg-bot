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
            KeyboardButton(text="📊 Исследования")
        ],
        [
            KeyboardButton(text="📋 Меню")
        ],
    ],
    resize_keyboard=True,
)

confirm_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔞 Я старше 18 лет, давай начнем", callback_data="confirm_18")]
        ]
    )

girls_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💃 Гера", callback_data="girl_hera"),
            InlineKeyboardButton(text="👠 Ева", callback_data="girl_eva"),
            InlineKeyboardButton(text="👸🏻 Вероника", callback_data="girl_veronika"),
            InlineKeyboardButton(text="👩🏻‍🦰 Кейт", callback_data="girl_kate"),
        ],
    ],
    resize_keyboard=True,
)

buy_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Написать", url="https://t.me/durov"),
        ],
    ]
)
