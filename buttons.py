from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_menu():
    inline_button = InlineKeyboardBuilder()

    inline_button.row(types.InlineKeyboardButton(
        text="Uzbek🇺🇿",
        callback_data="uz")
    )
    inline_button.row(types.InlineKeyboardButton(
        text="Русский🇷🇺",
        callback_data="ru")
    )
    inline_button.row(types.InlineKeyboardButton(
        text="Eng🇺🇸",
        callback_data="eng")
    )
    return inline_button.as_markup()
