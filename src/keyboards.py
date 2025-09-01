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

buy_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Написать", url="https://t.me/durov"),
        ],
    ]
)
