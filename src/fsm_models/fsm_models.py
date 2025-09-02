from aiogram.fsm.state import (
    State,
    StatesGroup,
)


class AgeConfirm(StatesGroup):
    not_confirmed = State()
    confirmed = State()

