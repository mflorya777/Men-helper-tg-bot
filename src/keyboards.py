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
    ], resize_keyboard=True
)

confirm_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔞 Я старше 18 лет, давай начнем", callback_data="confirm_18")]
        ]
    )

buy_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Написать", url="https://t.me/durov"),
        ],
    ]
)
