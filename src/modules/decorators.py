from functools import wraps

from aiogram.fsm.context import FSMContext
from aiogram import types

from src.fsm_models.fsm_models import AgeConfirm
from src.locales.i18n import get_locale


def require_age_confirmed(
    handler,
):
    @wraps(handler)
    async def wrapper(
        event,
        state: FSMContext = None,
        *args,
        **kwargs,
    ):
        if isinstance(event, types.Message):
            lang_code = event.from_user.language_code
        elif isinstance(event, types.CallbackQuery):
            lang_code = event.from_user.language_code
        else:
            lang_code = "ru"

        locale = get_locale(lang_code)

        current_state = await state.get_state() if state else None

        if current_state != AgeConfirm.confirmed:
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
        return await handler(
            event,
            state,
            *args,
            **kwargs,
        )
    return wrapper
