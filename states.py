from aiogram.fsm.state import StatesGroup, State


class ChatState(StatesGroup):
    waiting_for_msg = State()


class Language_State(StatesGroup):
    choosing_language = State()
    Eng = State()
    Rus = State()
    Uz = State


class AnonState(StatesGroup):
    waiting_for_reply = State()