from functools import wraps

from aiogram import types

from src.clients.mongo.mongo_client import MongoClient
from src.config import MongoConfig
from src.locales.i18n import get_locale


config = MongoConfig()
mongo_client = MongoClient(config)


def require_age_confirmed(
    handler,
):
    @wraps(handler)
    async def wrapper(
        event,
        *args,
        **kwargs,
    ):
        if isinstance(event, types.Message):
            user_id = event.from_user.id
            lang_code = event.from_user.language_code
        elif isinstance(event, types.CallbackQuery):
            user_id = event.from_user.id
            lang_code = event.from_user.language_code
        else:
            lang_code = "ru"
            user_id = None

        locale = get_locale(
            lang_code,
        )

        user = await mongo_client.get_user(
            user_id,
        )
        if not user or not user.is_age_confirmed:
            if isinstance(event, types.Message):
                await event.answer(
                    locale.decorator_confirm_18,
                )
            elif isinstance(event, types.CallbackQuery):
                await event.answer(
                    locale.decorator_confirm_18,
                    show_alert=True,
                )
            return

        if "user" in handler.__annotations__:
            kwargs["user"] = user

        return await handler(
            event,
            *args,
            **kwargs,
        )

    return wrapper
